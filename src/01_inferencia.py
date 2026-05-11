# ==============================================================================
# SCRIPT 01: INFERENCIA MASIVA Y ETIQUETADO DE SENTIMIENTO
# ==============================================================================
import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS DINÁMICAS (Arquitectura robusta)
# ------------------------------------------------------------------------------
# Calculamos la ruta base del proyecto (la carpeta TFG_Inteligencia_Datos)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definimos las rutas de entrada y salida
MODEL_PATH = os.path.join(BASE_DIR, "model", "cerebro_consumo_v3")  # <-- Roto entre modelos (el que mas me mole)
INPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "chatGPT_reviews.csv")  # <-- Asegúrate de que tu CSV se llama así
OUTPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_inferido2.csv")


# ------------------------------------------------------------------------------
# 2. PARÁMETROS DE INGENIERÍA (Hiperparámetros de ejecución)
# ------------------------------------------------------------------------------
BATCH_SIZE = 64  # Procesaremos las reseñas de 64 en 64 para no saturar la RAM
COLUMNA_TEXTO = "Review"  # <-- IMPORTANTE: Pon aquí el nombre exacto de la columna que tiene el texto en tu CSV original


def main():
    print("Iniciando Motor de Inferencia Masiva...")


    # A. Detección de Hardware (GPU si está disponible, si no, CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[-] Aceleración por hardware detectada: {device.type.upper()}")


    # B. Carga del "Cerebro" (Modelo y Tokenizador desde local)
    print("[-] Cargando el modelo pre-entrenado desde la carpeta local...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        model.to(device)
        model.eval()  # Modo evaluación (apaga funciones de entrenamiento como el Dropout)
    except Exception as e:
        print(f" X ERROR: No se ha encontrado el modelo en {MODEL_PATH}. ¿Has descargado y pegado la carpeta ahí?")
        return


    # C. Carga de los Datos en Bruto
    print(f"[-] Leyendo dataset masivo desde: {INPUT_DATA_PATH}")
    df = pd.read_csv(INPUT_DATA_PATH)

    # =========================================================
    # 1. CAPA DE ESTANDARIZACIÓN (MIGRACIÓN DE ESQUEMA)
    # =========================================================
    df.rename(columns={
        'reviewId': 'Review Id',
        'content': 'Review',
        'score': 'Ratings',
        'at': 'Review Date'
    }, inplace=True)

    # =========================================================
    # 2. LIMPIEZA FORENSE (Igual que en Colab Celda 3.2)
    # =========================================================
    print("[-] Aplicando limpieza estricta (Filtro Geográfico y Longitud)...")
    total_antes = len(df)

    # 2.1 Borramos nulos y duplicados
    df = df.dropna(subset=['Review', 'Review Date'])
    df = df.drop_duplicates(subset=['Review'])

    # 2.2 Filtro de Alfabeto no latino (Para que el modelo no alucine)
    patron_no_latino = r'[\u0400-\u04FF\u0600-\u06FF\u0900-\u097F\u3040-\u30FF\u4E00-\u9FFF]'
    df = df[~df['Review'].str.contains(patron_no_latino, na=False)]

    # 2.3 Filtro de longitud (> 20 caracteres)
    df = df[df['Review'].str.len() > 20]

    total_despues = len(df)
    print(f"[-] Limpieza finalizada. Descartados {total_antes - total_despues} registros basura/no latinos.")
    print(f"[-] Total de registros a inferir por la IA: {total_despues}")

    # Asegurarnos de que el texto es string
    df[COLUMNA_TEXTO] = df[COLUMNA_TEXTO].astype(str)
    textos = df[COLUMNA_TEXTO].tolist()


    # D. Bucle de Inferencia por Lotes (Batching)
    predicciones = []

    print("[-] Iniciando inferencia neuronal...")
    # tqdm nos pinta una barra de progreso preciosa en la consola
    for i in tqdm(range(0, len(textos), BATCH_SIZE), desc="Procesando batches"):
        lote_textos = textos[i:i + BATCH_SIZE]

        # 1. Tokenización matemática
        inputs = tokenizer(
            lote_textos,
            padding=True,
            truncation=True,
            max_length=256,  # Recortamos a 128 tokens por reseña para ganar velocidad
            return_tensors="pt"
        ).to(device)

        # 2. Inferencia estéril (torch.no_grad() evita fugas de memoria RAM)
        with torch.no_grad():
            outputs = model(**inputs)
            # Extraemos la clase ganadora de las probabilidades
            lote_predicciones = torch.argmax(outputs.logits, dim=-1).cpu().tolist()

        predicciones.extend(lote_predicciones)


    # E. Transformación de salida y Guardado
    # Mapeamos los números (0, 1, 2) a las etiquetas reales (-1, 0, 1) que tenías en Colab
    # *Ajusta este diccionario si tu modelo en Colab mapeó diferente*
    mapa_sentimiento = {0: -1, 1: 0, 2: 1}
    df['Sentimiento_IA'] = [mapa_sentimiento.get(p, p) for p in predicciones]

    print(f"[-] Inferencia completada. Guardando resultados en: {OUTPUT_DATA_PATH}")
    df.to_csv(OUTPUT_DATA_PATH, index=False)

    print(" ¡PROCESO FINALIZADO! La 'Máquina' ha hecho su trabajo.")


if __name__ == "__main__":
    main()