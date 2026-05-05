# ==============================================================================
# SCRIPT 03: DASHBOARD FORENSE DE SENTIMIENTO (VERSIÓN PRO VIBRANTE)
# ==============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. CONFIGURACIÓN DE ESTÉTICA AVANZADA ---
st.set_page_config(page_title="ChatGPT Intelligence Pulse", page_icon="🧠", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8fafc; }

    div[data-testid="stMetric"] {
        background-color: white !important; border-radius: 15px; padding: 15px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #f1f5f9; height: 140px; 
        display: flex; flex-direction: column; justify-content: center;
    }
    div[data-testid="stMetricLabel"] * { color: #64748b !important; font-weight: 600 !important; font-size: 1.05rem !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] div { color: #0891b2 !important; font-weight: 800 !important; }

    .stPlotlyChart {
        background-color: white !important; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        padding: 15px; border: 1px solid #f1f5f9;
    }

    .status-box {
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
        border-left: 5px solid #0891b2; background-color: #ecfeff !important;
        min-height: 180px; display: flex; flex-direction: column; justify-content: center;
    }
    .status-box p, .status-box b, .status-box i { color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)


# --- 2. POPUP INTERACTIVO (ST.DIALOG) ---
@st.dialog("🔬 Autopsia del Evento")
def mostrar_detalles_evento(fecha_str, evento, tipo, color, sentimiento, volumen, avg_sentimiento):
    st.markdown(f"<h3 style='color: {color}; margin-bottom: 0;'>{evento}</h3>", unsafe_allow_html=True)
    st.markdown(f"**Fecha:** {fecha_str} | **Categoría:** {tipo}")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        delta_val = sentimiento - avg_sentimiento
        color_delta = "#10b981" if delta_val >= 0 else "#f43f5e"
        bg_delta = "#d1fae5" if delta_val >= 0 else "#ffe4e6"
        flecha = "↑" if delta_val >= 0 else "↓"

        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 15px; border: 1px solid #e2e8f0; height: 100%;">
            <p style="color: #64748b; font-size: 0.85rem; font-weight: 700; margin: 0; text-transform: uppercase;">Sentimiento del Día</p>
            <p style="color: #0891b2; font-size: 1.8rem; font-weight: 800; margin: 0; line-height: 1.2;">{sentimiento:.3f}</p>
            <p style="color: {color_delta}; background-color: {bg_delta}; font-size: 0.85rem; font-weight: 700; width: max-content; padding: 2px 8px; border-radius: 10px; margin: 0; margin-top: 5px;">{flecha} {abs(delta_val):.3f} vs Media</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 15px; border: 1px solid #e2e8f0; height: 100%;">
            <p style="color: #64748b; font-size: 0.85rem; font-weight: 700; margin: 0; text-transform: uppercase;">Volumen de Reseñas</p>
            <p style="color: #0891b2; font-size: 1.8rem; font-weight: 800; margin: 0; line-height: 1.2;">{volumen:,}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if tipo == "Incidente Técnico":
        st.error(
            "📉 **Análisis Forense:** Los incidentes técnicos provocan las caídas más bruscas y rápidas en la confianza del consumidor. El usuario penaliza severamente la falta de disponibilidad.")
    elif tipo == "Crisis Corporativa":
        st.warning(
            "⚖️ **Análisis Forense:** A pesar de la gravedad mediática, los datos demuestran que el consumidor final es altamente resiliente a los dramas de liderazgo mientras la herramienta siga funcionando.")
    elif tipo == "Lanzamiento":
        st.success(
            "🚀 **Análisis Forense:** Los anuncios de nuevas capacidades generan picos de adopción, aunque a veces vienen seguidos de caídas temporales por saturación de servidores.")
    else:
        st.info(
            "📊 **Análisis Forense:** Hito estadístico significativo que marca un cambio de tendencia en el comportamiento de la comunidad de usuarios.")



# --- 3. CARGA DE DATOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "serie_temporal_lineaA.csv"))
    df['Review Date'] = pd.to_datetime(df['Review Date'])
    df = df.rename(columns={'Review Date': 'Fecha', 'Sentimiento_Medio': 'Sentimiento', 'Volumen_Reseñas': 'Volumen'})

    df_eventos = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "eventos", "eventos_openai.csv"))
    df_eventos['Fecha'] = pd.to_datetime(df_eventos['Fecha'])
    color_map = {"Lanzamiento": "#10b981", "Incidente Técnico": "#f43f5e", "Crisis Corporativa": "#f59e0b",
                 "Hito Analítico": "#8b5cf6"}
    df_eventos['Color'] = df_eventos['Tipo'].map(lambda x: color_map.get(x, "#94a3b8"))

    # Cruzar eventos con datos reales para el gráfico
    df_eventos = df_eventos.merge(df, on='Fecha', how='inner')
    return df, df_eventos


try:
    df, df_events = load_data()
except FileNotFoundError:
    st.error("❌ Archivos no encontrados.")
    st.stop()



# --- 4. DASHBOARD UI Y KPIs ---
st.title("🧠 ChatGPT Intelligence Pulse")
st.markdown("Análisis forense del sentimiento del mercado y eventos disruptivos (2023-2024).")

max_day = df.loc[df['Sentimiento'].idxmax()]
min_day = df.loc[df['Sentimiento'].idxmin()]
avg_sentimiento_global = df['Sentimiento'].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div style="background-color: white; border-radius: 15px; padding: 15px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #f1f5f9; height: 130px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #64748b; font-size: 0.9rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">Volumen Total</p>
        <p style="color: #0891b2; font-size: 2.2rem; font-weight: 800; margin: 0; line-height: 1.2;">{df['Volumen'].sum():,}</p>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div style="background-color: white; border-radius: 15px; padding: 15px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #f1f5f9; height: 130px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #64748b; font-size: 0.9rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">Sentimiento Avg</p>
        <p style="color: #0891b2; font-size: 2.2rem; font-weight: 800; margin: 0; line-height: 1.2;">{avg_sentimiento_global:.3f}</p>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div style="background-color: white; border-radius: 15px; padding: 15px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #f1f5f9; height: 130px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #64748b; font-size: 0.9rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">Pico Positivo</p>
        <p style="color: #0891b2; font-size: 2rem; font-weight: 800; margin: 0; line-height: 1.2;">{max_day['Fecha'].strftime('%d %b %y')}</p>
        <p style="color: #10b981; background-color: #d1fae5; font-size: 0.9rem; font-weight: 700; margin: 0; width: max-content; padding: 2px 8px; border-radius: 10px; margin-top: 5px;">↑ {max_day['Sentimiento']:.3f}</p>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div style="background-color: white; border-radius: 15px; padding: 15px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #f1f5f9; height: 130px; display: flex; flex-direction: column; justify-content: center;">
        <p style="color: #64748b; font-size: 0.9rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">Valle Crítico</p>
        <p style="color: #0891b2; font-size: 2rem; font-weight: 800; margin: 0; line-height: 1.2;">{min_day['Fecha'].strftime('%d %b %y')}</p>
        <p style="color: #f43f5e; background-color: #ffe4e6; font-size: 0.9rem; font-weight: 700; margin: 0; width: max-content; padding: 2px 8px; border-radius: 10px; margin-top: 5px;">↓ {min_day['Sentimiento']:.3f}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")



# --- 5. GRÁFICO PRINCIPAL INTERACTIVO ---
st.subheader("📊 Línea de Tiempo Forense")

fig = go.Figure()

# Área de Volumen y Línea de Sentimiento
fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Volumen'], fill='tozeroy', name='Volumen',
                         line=dict(width=0.5, color='rgba(139, 92, 246, 0.3)'), fillcolor='rgba(139, 92, 246, 0.15)',
                         yaxis='y2'))
fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Sentimiento'], mode='lines', name='Sentimiento Medio',
                         line=dict(color='#0891b2', width=3, shape='spline'), yaxis='y1'))

# Novedad: Puntos remarcados sobre la línea
fig.add_trace(go.Scatter(
    x=df_events['Fecha'], y=df_events['Sentimiento'],
    mode='markers', name='Eventos Clave',
    marker=dict(size=12, color=df_events['Color'], line=dict(width=2, color='white')),
    yaxis='y1', hoverinfo='text', hovertext=df_events['Evento']
))

# Zona sombreada crítica
fig.add_vrect(x0="2023-07-31", x1="2023-08-05", fillcolor="#f43f5e", opacity=0.15, layer="below", line_width=0,
              annotation_text="Degradación Crítica", annotation_position="top left", annotation_font_color="#f43f5e")

# Anotaciones con algoritmo anti-solapamiento
alturas_ay = [-50, -100, -150, -70]  # Patrón de alturas
for i, row in df_events.iterrows():
    ay_dinamico = alturas_ay[i % len(alturas_ay)]
    fig.add_annotation(
        x=row['Fecha'], y=row['Sentimiento'], text=f"<b>{row['Evento']}</b>",
        showarrow=True, arrowhead=2, arrowcolor=row['Color'],
        ax=0, ay=ay_dinamico, bgcolor=row['Color'], font=dict(color="white", size=10),
        borderpad=4, bordercolor=row['Color'], borderwidth=1
    )

fig.update_layout(
    template="plotly_white", hovermode="x unified", height=600, margin=dict(t=30, b=30, l=50, r=50),
    yaxis=dict(title="<b>Sentimiento (0 a 1)</b>", range=[-0.2, 1], gridcolor="#f1f5f9"),
    yaxis2=dict(title="<b>Volumen</b>", overlaying='y', side="right", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)



# --- 6. BOTONERA DE POPUPS (LA "PILLERÍA") ---
st.markdown("👆 **Analizador de Eventos:** Haz clic en un evento para abrir su autopsia estadística.")
# Crear filas de botones dinámicamente
cols = st.columns(5)
for i, row in df_events.iterrows():
    with cols[i % 5]:
        if st.button(f"🔍 {row['Fecha'].strftime('%d %b')}", key=f"btn_{i}", use_container_width=True):
            mostrar_detalles_evento(
                row['Fecha'].strftime('%d %b %Y'), row['Evento'], row['Tipo'],
                row['Color'], row['Sentimiento'], row['Volumen'], avg_sentimiento_global
            )


# --- 7. INSIGHTS (TEXTO ORIGINAL) ---
st.markdown("---")
st.markdown("### 💡 Insights del Análisis Forense")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="status-box" style="border-left-color: #f43f5e; background-color: #fff1f2 !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>📉 Impacto del Rendimiento Técnico:</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">La zona sombreada (31 Jul - 05 Ago 2023) demuestra que <b>los incidentes técnicos son el mayor destructor de valor</b>. La retirada del <i>AI Classifier</i> y la percepción de que GPT-4 se había vuelto "perezoso" provocaron una degradación sostenida de casi una semana, hundiendo el sentimiento al mínimo histórico absoluto (0.108).</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="status-box" style="border-left-color: #f59e0b; background-color: #fffbeb !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>🛡️ La Inmunidad al Drama Corporativo:</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">A diferencia de los fallos técnicos, los datos revelan que <b>el consumidor final es resiliente a las crisis de liderazgo</b>. Durante el despido y retorno de Sam Altman (17-22 Nov), el sentimiento apenas descendió a valores neutros (0.49), demostrando que la opinión pública valora la utilidad del producto muy por encima de la inestabilidad directiva.</p>
    </div>
    """, unsafe_allow_html=True)



# --- 8. POPUPS PARA GRÁFICAS INFERIORES ---
@st.dialog("📚 Explicación: Sentimiento por Tipo")
def popup_barras():
    st.markdown("### Clasificación Histórica")
    st.write(
        "Este gráfico agrupa los datos de todo el año basándose en el calendario de eventos de la **Línea B**. Demuestra empíricamente que los incidentes técnicos (en rojo) generan un impacto negativo desproporcionado en la percepción del usuario, mientras que los lanzamientos y la operativa normal mantienen promedios estables de aprobación superior al 53%.")


@st.dialog("📚 Explicación: Volumen vs Sentimiento")
def popup_scatter():
    st.markdown("### Análisis de Dispersión y Tendencia")
    st.write(
        "Muestra la correlación entre la cantidad de reseñas diarias (eje X) y el nivel de satisfacción (eje Y). La línea de regresión (Lowess) en rojo evidencia un patrón interesante: **los picos anómalos de volumen suelen estar asociados a caídas drásticas de sentimiento**, lo que confirma que el usuario medio acude masivamente a las tiendas de aplicaciones principalmente cuando el servicio falla.")



# --- 9. CORRELACIÓN Y CATEGORÍAS (GRÁFICOS MEJORADOS) ---
st.write("---")
row2_1, row2_2 = st.columns([1, 1])

with row2_1:
    col_tit1, col_btn1 = st.columns([0.85, 0.15])
    with col_tit1: st.subheader("🏆 Sentimiento por Evento")
    with col_btn1:
        if st.button("ℹ️ Info", key="btn_info_bar", use_container_width=True): popup_barras()

    # Preparación de datos para barras
    df_merged = df.merge(df_events[['Fecha', 'Tipo']], on='Fecha', how='left')
    df_merged['Tipo'] = df_merged['Tipo'].fillna('Día Normal')
    cat_avg = df_merged.groupby('Tipo')['Sentimiento'].mean().sort_values().reset_index()

    fig_bar = px.bar(
        cat_avg, x='Sentimiento', y='Tipo', orientation='h',
        color='Tipo', color_discrete_map={
            'Lanzamiento': '#10b981', 'Crisis Corporativa': '#f59e0b',
            'Incidente Técnico': '#f43f5e', 'Hito Analítico': '#8b5cf6', 'Día Normal': '#94a3b8'
        }, text_auto='.3f'
    )
    fig_bar.update_layout(showlegend=False, height=380, template="plotly_white", margin=dict(l=10, r=20, t=10, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_2:
    col_tit2, col_btn2 = st.columns([0.85, 0.15])
    with col_tit2: st.subheader("🎯 Volumen vs Sentimiento")
    with col_btn2:
        if st.button("ℹ️ Info", key="btn_info_scat", use_container_width=True): popup_scatter()

    fig_scat = px.scatter(
        df, x="Volumen", y="Sentimiento", color="Sentimiento",
        color_continuous_scale="Viridis", trendline="lowess", trendline_color_override="#f43f5e"
    )
    fig_scat.update_layout(height=380, template="plotly_white", margin=dict(l=10, r=20, t=10, b=20))
    st.plotly_chart(fig_scat, use_container_width=True)

st.markdown("<br><center><small>Validación de Datos v3.0 | Pipeline de Inteligencia Híbrida</small></center>",
            unsafe_allow_html=True)