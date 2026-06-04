# 📊 Análisis Forense de Sentimiento: OpenAI y ChatGPT

Proyecto de Inteligencia de Datos y Machine Learning (TFG) diseñado para analizar la evolución del sentimiento público hacia ChatGPT mediante inferencia masiva y correlación de eventos.

Marcos García Benito.

## 🏗️ Arquitectura del Proyecto (Híbrida)

El proyecto se divide en tres fases estratégicas:

* **Fase 1: El "Cerebro" (Cloud / Google Colab).** Ajuste fino (*Fine-Tuning*) de un modelo Transformer multilingüe (`XLM-RoBERTa`) utilizando una muestra estratificada de 45.000 registros (15.000 por clase). Esta arquitectura permite una detección de sentimiento (Negativo, Neutro, Positivo) precisa y a escala global, eliminando las barreras idiomáticas.
* **Fase 2: La "Máquina" (Local / PyCharm).** Inferencia masiva sobre un dataset inicial de **+1.000.000 de reseñas**. Implementación de un pipeline ETL avanzado para aplicar una limpieza forense estricta (filtros anti-bots y control de ruido), reteniendo ~350.000 opiniones humanas genuinas con las que se genera la serie temporal estadísticamente validada (Línea A).
* **Fase 3: El "Escaparate" (Dashboard).** Correlación de la Línea A con eventos históricos de OpenAI (2023-2026) mediante un Dashboard de Business Intelligence. El sistema audita fenómenos complejos como el "Sentiment Lag" (latencia ante incidentes técnicos) y la resiliencia del consumidor ante crisis corporativas.

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

````

## 🚀 Manual de Uso y Ejecución

Para facilitar la evaluación de este proyecto, el repositorio está preparado para ejecutarse en dos modalidades diferentes:

### Despliegue Rápido (Solo Visualización del Dashboard)
Si deseas ver directamente los resultados y la interfaz interactiva sin necesidad de descargar el modelo masivo ni procesar los datos en bruto, sigue estos pasos:

1. Clona este repositorio y crea un entorno virtual.
2. Instala las dependencias: `pip install -r requirements.txt`
3. En la carpeta `data/processed/` y `data/raw/eventos/` ya se incluyen los CSV finales (`serie_temporal_lineaA.csv` y `eventos_openai.csv`) de peso ligero.
4. Levanta el servidor local ejecutando:
   `streamlit run src/03_dashboard.py`
5. El *Dashboard* interactivo se abrirá automáticamente en tu navegador.

OJO : Para el flujo completo pidele al dueño el repo completo (Para evaluación académica en la entrega final del TFG)
