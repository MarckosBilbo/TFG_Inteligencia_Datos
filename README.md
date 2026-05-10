# 📊 Análisis Forense de Sentimiento: OpenAI y ChatGPT

Proyecto de Inteligencia de Datos y Machine Learning (TFG) diseñado para analizar la evolución del sentimiento público hacia ChatGPT mediante inferencia masiva y correlación de eventos.

## 🏗️ Arquitectura del Proyecto (Híbrida)

El proyecto se divide en tres fases estratégicas:

* **Fase 1: El "Cerebro" (Cloud / Google Colab).** Fine-Tuning de un modelo Transformer (`Twitter-RoBERTa`) con 15.000 registros balanceados para la detección precisa del sentimiento (Negativo, Neutro, Positivo).
* **Fase 2: La "Máquina" (Local / PyCharm).** Inferencia masiva sobre +190.000 reseñas utilizando el modelo persistido. Pipeline ETL para aplicar limpieza forense (filtros anti-bots) y generar la serie temporal (Línea A).
* **Fase 3: El "Escaparate" (Dashboard).** Correlación de la Línea A con eventos históricos de OpenAI mediante un Dashboard interactivo de Business Intelligence.

## 📂 Estructura del Repositorio local
* `/src`: Scripts ejecutables de inferencia, ETL y visualización.
* `/model`: Ubicación del modelo pre-entrenado (excluido en .gitignore por peso).
* `/data`: Datasets raw y processed (archivos masivos excluidos en .gitignore).
* `Extras`: Añadidos en la raíz el `.gitignore`, `README.md` y `requirements.txt`.

Para evitar saturar el repositorio y cumplir con las buenas prácticas, los archivos masivos de datos (.csv) y los pesos del modelo están excluidos mediante `.gitignore`.

```text
TFG_Inteligencia_Datos/
│
├── data/                       # ⚠️ Archivos masivos excluidos de GIT
│   ├── raw/                    # -> Colocar aquí: ChatGPT_Reviews.csv (Dataset original)
│   │   └── eventos/            # Catálogo manual de hitos históricos
│   │       └── eventos_openai.csv 
│   └── processed/              # -> Aquí se autogenerarán: dataset_inferido.csv y serie_temporal_lineaA.csv
│
├── model/                      # ⚠️ EXCLUIDO DE GIT (Añadir manualmente)
│   └── cerebro_consumo_v2/     # -> Colocar aquí: Pesos, config y tokenizador de Hugging Face
│
├── src/                        # Código fuente de producción
│   ├── 01_inferencia.py        # Motor de etiquetado masivo por lotes con PyTorch
│   ├── 02_etl_temporal.py      # Limpieza forense con Pandas y compresión a serie temporal
│   └── 03_dashboard.py         # Interfaz web analítica (BI) interactiva con Streamlit y Plotly
│
├── .gitignore                  # Reglas de exclusión de seguridad
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias del entorno virtual
