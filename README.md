#  Análisis Forense de Sentimiento: OpenAI y ChatGPT

Proyecto de Inteligencia de Datos y Machine Learning (TFG) diseñado para analizar la evolución del sentimiento público hacia ChatGPT mediante inferencia masiva y correlación de eventos.

##  Arquitectura del Proyecto (Híbrida)

El proyecto se divide en tres fases estratégicas:

*    **Fase 1: El "Cerebro" (Cloud / Google Colab).** Fine-Tuning de un modelo Transformer (`Twitter-RoBERTa`) con 15.000 registros balanceados para la detección precisa del sentimiento (Negativo, Neutro, Positivo).
*    **Fase 2: La "Máquina" (Local / PyCharm).** Inferencia masiva sobre +190.000 reseñas utilizando el modelo persistido. Pipeline ETL para aplicar limpieza forense (filtros anti-bots) y generar la serie temporal (Línea A).
*    **Fase 3: El "Escaparate" (En desarrollo).** Correlación de la Línea A con eventos históricos de OpenAI mediante un Dashboard interactivo.

## 📂 Estructura del Repositorio local
* `/src`: Scripts ejecutables de inferencia y ETL.
* `/notebooks`: Respaldos de los cuadernos de investigación en la nube.
* `/model`: Ubicación del modelo pre-entrenado (excluido en .gitignore por peso).
* `/data`: Datasets raw y processed (excluidos en .gitignore por peso).


Para evitar saturar el repositorio y cumplir con las buenas prácticas, los archivos masivos de datos y los pesos del modelo están excluidos mediante `.gitignore`.

```text
TFG_Inteligencia_Datos/
│
├── data/                       # ⚠️ EXCLUIDO DE GIT (Añadir manualmente)
│   ├── raw/                    # -> Colocar aquí: ChatGPT_Reviews.csv (Dataset original)
│   └── processed/              # -> Aquí se autogenerarán: dataset_inferido.csv y serie_temporal_lineaA.csv
│
├── model/                      # ⚠️ EXCLUIDO DE GIT (Añadir manualmente)
│   └── cerebro_consumo_v2/     # -> Colocar aquí: Pesos, config y tokenizador de Hugging Face exportados en Fase 1
│
├── notebooks/                  
│   └── Mundo_B_ChatGPT.ipynb   # Respaldo del cuaderno de entrenamiento (Fase 1 en Google Colab)
│
├── src/                        # Código fuente de producción
│   ├── 01_inferencia.py        # Motor de etiquetado masivo por lotes con PyTorch
│   └── 02_etl_temporal.py      # Limpieza forense con Pandas y compresión a serie temporal
│
├── .gitignore                  # Reglas de exclusión de seguridad
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias del entorno virtual
