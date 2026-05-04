# ==============================================================================
# SCRIPT 02: PIPELINE ETL Y AGRUPACIÓN TEMPORAL (LÍNEA A)
# ==============================================================================
import os
import pandas as pd

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# ------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_inferido.csv")
OUTPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "serie_temporal_lineaA.csv")


def main():
    print("🚀 Iniciando Pipeline ETL (Extracción, Transformación y Carga)...")

    # A. EXTRACCIÓN (Extract)
    print(f"[-] Leyendo dataset inferido desde: {INPUT_DATA_PATH}")
    try:
        df = pd.read_csv(INPUT_DATA_PATH)
    except FileNotFoundError:
        print(f" ERROR: No se encuentra el archivo {INPUT_DATA_PATH}. ¿Terminó el Script 01?")
        return

    total_inicial = len(df)
    print(f"[-] Registros iniciales cargados: {total_inicial}")

    # B. TRANSFORMACIÓN (Transform) - LIMPIEZA FORENSE
    print("[-] Aplicando reglas de Limpieza Forense...")

    # 1. Eliminar filas sin fecha o sin texto
    df = df.dropna(subset=['Review', 'Review Date'])

    # 2. Eliminar duplicados exactos (Filtro Anti-Bots)
    df = df.drop_duplicates(subset=['Review'])

    # 3. Eliminar reseñas de menos de 3 palabras (Ruido: "good", "nice app")
    # Convertimos a string por si acaso, separamos por espacios y contamos
    df['Review'] = df['Review'].astype(str)
    df = df[df['Review'].str.split().str.len() >= 3]

    total_limpio = len(df)
    registros_borrados = total_inicial - total_limpio
    print(f"[-] Limpieza completada: Se han eliminado {registros_borrados} registros (ruido/bots).")
    print(f"[-] Registros útiles para el análisis: {total_limpio}")

    # C. TRANSFORMACIÓN (Transform) - AGRUPACIÓN TEMPORAL
    print("[-] Procesando series temporales...")

    # Convertir la columna de texto a formato Fecha (Date) estándar (Año-Mes-Día)
    # coerce convierte errores en NaT (Not a Time) por si hay fechas corruptas
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce').dt.date
    df = df.dropna(subset=['Review Date'])  # Tiramos fechas corruptas

    # Agrupar por Día: Calculamos la MEDIA del sentimiento y el RECUENTO de volumen
    df_temporal = df.groupby('Review Date').agg(
        Sentimiento_Medio=('Sentimiento_IA', 'mean'),
        Volumen_Reseñas=('Review', 'count')
    ).reset_index()

    # Ordenar cronológicamente
    df_temporal = df_temporal.sort_values(by='Review Date')

    # D. CARGA (Load)
    print(f"[-] Guardando Serie Temporal en: {OUTPUT_DATA_PATH}")
    df_temporal.to_csv(OUTPUT_DATA_PATH, index=False)

    print(" ¡PIPELINE ETL FINALIZADO! La 'Línea A' está lista para el Dashboard.")


if __name__ == "__main__":
    main()