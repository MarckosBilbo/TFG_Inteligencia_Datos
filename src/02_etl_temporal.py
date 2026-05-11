# ==============================================================================
# SCRIPT 02: PIPELINE ETL Y AGRUPACIÓN TEMPORAL (LÍNEA A) - VERSIÓN FINAL
# ==============================================================================
import os
import pandas as pd

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# ------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_inferido2.csv")
OUTPUT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "serie_temporal_lineaA2.csv")


def main():
    print("🚀 Iniciando Pipeline ETL (Extracción, Transformación y Carga)...")

    # A. EXTRACCIÓN (Extract)
    print(f"[-] Leyendo dataset inferido desde: {INPUT_DATA_PATH}")
    try:
        df = pd.read_csv(INPUT_DATA_PATH)
    except FileNotFoundError:
        print(f" ❌ ERROR: No se encuentra el archivo {INPUT_DATA_PATH}. ¿Terminó el Script 01?")
        return

    total_inicial = len(df)
    print(f"[-] Registros iniciales cargados: {total_inicial}")

    # B. TRANSFORMACIÓN (Transform) - AGRUPACIÓN TEMPORAL
    print("[-] Procesando series temporales...")

    # 1. Convertir a Fecha estándar (Año-Mes-Día) y eliminar fechas corruptas
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce').dt.date
    df = df.dropna(subset=['Review Date'])

    # 2. Agrupar por Día: Calculamos MEDIA de sentimiento y RECUENTO de volumen
    df_temporal = df.groupby('Review Date').agg(
        Sentimiento_Medio=('Sentimiento_IA', 'mean'),
        Volumen_Reseñas=('Review', 'count')
    ).reset_index()

    # 3. Ordenar cronológicamente
    df_temporal = df_temporal.sort_values(by='Review Date')

    # =====================================================================
    # C. FILTRO ANTI-RUIDO (EL "TRUNCADO")
    # =====================================================================
    dias_antes = len(df_temporal)

    # Cortamos los días que tengan menos de 100 reseñas (Ajusta este número si quieres)
    # 100 es un buen umbral para un dataset de 1 Millón. Los días de 1, 2 o 10 reseñas desaparecen.
    UMBRAL_RESEÑAS = 100
    df_temporal = df_temporal[df_temporal['Volumen_Reseñas'] >= UMBRAL_RESEÑAS]

    dias_despues = len(df_temporal)
    print(
        f"[-] Limpieza de ruido: Se han truncado {dias_antes - dias_despues} días por falta de volumen (< {UMBRAL_RESEÑAS} reseñas).")
    # =====================================================================

    # D. CARGA (Load)
    print(f"[-] Guardando Serie Temporal en: {OUTPUT_DATA_PATH}")
    df_temporal.to_csv(OUTPUT_DATA_PATH, index=False)

    print("✅ ¡PIPELINE ETL FINALIZADO! La curva de sentimiento real está lista.")


if __name__ == "__main__":
    main()