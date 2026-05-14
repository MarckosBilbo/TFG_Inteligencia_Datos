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
            "📉 **Análisis Forense:** Caída súbita del servicio. El usuario penaliza severamente la falta de disponibilidad en el corto plazo.")
    elif tipo == "Desencadenante":
        st.error(
            "📉 **Análisis Forense (Latencia):** Evento que inicia una crisis. Empíricamente, la frustración del usuario requiere una ventana de 3 a 7 días para consolidarse como un colapso en las métricas de sentimiento.")
    elif tipo == "Crisis Corporativa":
        st.warning(
            "⚖️ **Análisis Forense:** El consumidor final es altamente resiliente a los dramas de liderazgo (nivel corporativo) mientras la herramienta siga operativa.")
    elif tipo == "Lanzamiento":
        st.success(
            "🚀 **Análisis Forense:** Los anuncios de nuevas capacidades generan picos de adopción, aunque en ocasiones saturan la red en los días posteriores.")
    else:
        st.info(
            "📊 **Análisis Forense:** Hito estadístico o corporativo significativo.")



# --- 3. CARGA DE DATOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "serie_temporal_lineaA2.csv"))
    df['Review Date'] = pd.to_datetime(df['Review Date'])
    df = df.rename(columns={'Review Date': 'Fecha', 'Sentimiento_Medio': 'Sentimiento', 'Volumen_Reseñas': 'Volumen'})

    df_eventos = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "eventos", "eventos_openai.csv"))
    df_eventos['Fecha'] = pd.to_datetime(df_eventos['Fecha'])

    # Manejar la nueva columna Fecha_Fin (si está vacía será NaT)
    if 'Fecha_Fin' in df_eventos.columns:
        df_eventos['Fecha_Fin'] = pd.to_datetime(df_eventos['Fecha_Fin'], errors='coerce')

    # Nuevos colores mapeados
    color_map = {
        "Lanzamiento": "#10b981",  # Verde
        "Incidente Técnico": "#f43f5e",  # Rojo
        "Desencadenante": "#f97316",  # Naranja
        "Crisis Corporativa": "#f59e0b",  # Amarillo/Naranja
        "Hito Clave": "#7c3aed",  # Morado Eléctrico (Para los picos/valles)
        "Evento Corporativo": "#3b82f6",  # Azul Wall Street
        "Hito Analítico": "#8b5cf6"  # Morado claro
    }
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
st.markdown("Análisis forense del sentimiento del mercado y adopción tecnológica (2023-2026).")

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

# Anotaciones con algoritmo anti-solapamiento y Cajas de Sombreado Dinámicas
alturas_ay = [-50, -100, -150, -70]  # Patrón de alturas

for i, row in df_events.iterrows():
    # 1. Añadimos el cartelito
    ay_dinamico = alturas_ay[i % len(alturas_ay)]
    fig.add_annotation(
        x=row['Fecha'], y=row['Sentimiento'], text=f"<b>{row['Evento']}</b>",
        showarrow=True, arrowhead=2, arrowcolor=row['Color'],
        ax=0, ay=ay_dinamico, bgcolor=row['Color'], font=dict(color="white", size=10),
        borderpad=4, bordercolor=row['Color'], borderwidth=1
    )

    # 2. Si el evento es multicapa (tiene Fecha_Fin), dibujamos el sombreado vertical
    if 'Fecha_Fin' in df_events.columns and pd.notna(row['Fecha_Fin']):
        fig.add_vrect(
            x0=row['Fecha'],
            x1=row['Fecha_Fin'],
            fillcolor=row['Color'],  # Toma el color del evento (naranja)
            opacity=0.15,
            layer="below",
            line_width=0
        )

# Puntos remarcados sobre la línea
fig.add_trace(go.Scatter(
    x=df_events['Fecha'], y=df_events['Sentimiento'],
    mode='markers', name='Eventos Clave',
    marker=dict(size=12, color=df_events['Color'], line=dict(width=2, color='white')),
    yaxis='y1', hoverinfo='text', hovertext=df_events['Evento']
))

fig.update_layout(
    template="plotly_white", hovermode="x unified", height=600, margin=dict(t=30, b=30, l=50, r=50),
    yaxis=dict(title="<b>Sentimiento (0 a 1)</b>", range=[-0.2, 1], gridcolor="#f1f5f9"),
    yaxis2=dict(title="<b>Volumen</b>", overlaying='y', side="right", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)



# --- 6. BOTONERA DE POPUPS ---
st.markdown("👆 **Analizador de Eventos:** Haz clic en un evento para abrir su autopsia estadística.")
# Crear filas de botones dinámicamente
cols = st.columns(5)
for i, row in df_events.iterrows():
    with cols[i % 5]:
        if st.button(f"🔍 {row['Fecha'].strftime('%d %b %y')}", key=f"btn_{i}", use_container_width=True):
            mostrar_detalles_evento(
                row['Fecha'].strftime('%d %b %Y'), row['Evento'], row['Tipo'],
                row['Color'], row['Sentimiento'], row['Volumen'], avg_sentimiento_global
            )



# --- 7. INSIGHTS DEL ANÁLISIS FORENSE ---
st.markdown("---")
st.markdown("### 💡 Insights del Análisis Forense")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="status-box" style="border-left-color: #f97316; background-color: #fff7ed !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>📉 El Fenómeno del "Sentiment Lag" (Latencia):</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">Las crisis técnicas no se reflejan instantáneamente. Un evento desencadenante genera una <b>ventana de degradación de 3 a 7 días</b> hasta que la masa crítica de frustración indexa el sentimiento en su punto más bajo (Valle Crítico).</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="status-box" style="border-left-color: #f59e0b; background-color: #fffbeb !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>🛡️ La Inmunidad al Drama Corporativo:</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">A diferencia de los fallos técnicos, los datos revelan que <b>el consumidor final es resiliente a las crisis de liderazgo</b>. El núcleo de usuarios valora la utilidad estricta del producto, penalizándolo severamente únicamente cuando la disponibilidad técnica colapsa.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="status-box" style="border-left-color: #7c3aed; background-color: #f5f3ff !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>🏆 Máximo Histórico (Pico de Optimismo):</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">Registrado el 20 de Ago de 2024. Coincide con el despliegue del <i>Advanced Voice Mode</i>. Empíricamente, es el momento en el que el modelo <b>supera la barrera de la utilidad algorítmica para generar empatía</b> real en la comunidad, disparando el sentimiento positivo a niveles sin precedentes.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="status-box" style="border-left-color: #ef4444; background-color: #fef2f2 !important;">
        <p style="color: #0f172a !important; margin-bottom: 5px;"><b>⚠️ Mínimo Histórico (Anomalía Detectada):</b></p>
        <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5;">Registrado el 8 de Oct de 2024. La IA detectó el <b>colapso de confianza más severo del dataset (-0.14)</b>, sin que mediara un comunicado oficial corporativo. Esto sugiere un fallo profundo de base de datos o un ajuste agresivo en los filtros (censura) que castigó la experiencia de usuario real.</p>
    </div>
    """, unsafe_allow_html=True)



# --- 8. ANÁLISIS DE CATEGORÍAS (BARRAS Y SALUD) ---
st.write("---")
row2_1, row2_2 = st.columns([1, 1])

with row2_1:
    st.subheader("📊 Sentimiento por Categoría Base")
    # Filtrado estricto para mostrar solo las categorías con sentido promediable
    df_merged = df.merge(df_events[['Fecha', 'Tipo']], on='Fecha', how='left')
    df_merged['Tipo'] = df_merged['Tipo'].fillna('Día Normal')
    tipos_permitidos = ['Lanzamiento', 'Incidente Técnico', 'Crisis Corporativa', 'Día Normal']

    df_filtrado = df_merged[df_merged['Tipo'].isin(tipos_permitidos)]
    cat_avg = df_filtrado.groupby('Tipo')['Sentimiento'].mean().sort_values().reset_index()

    fig_bar = px.bar(
        cat_avg, x='Sentimiento', y='Tipo', orientation='h',
        color='Tipo', color_discrete_map={
            'Lanzamiento': '#10b981', 'Crisis Corporativa': '#f59e0b',
            'Incidente Técnico': '#f43f5e', 'Día Normal': '#94a3b8'
        }, text_auto='.3f'
    )
    fig_bar.update_layout(showlegend=False, height=350, template="plotly_white", margin=dict(l=10, r=20, t=10, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_2:
    st.subheader("🍩 Distribución de Salud del Producto")


    # Categorizamos los días según su sentimiento global
    def clasificar_salud(s):
        if s >= 0.55:
            return 'Óptima (>= 0.55)'
        elif s >= 0.40:
            return 'Estable (0.40 - 0.54)'
        else:
            return 'Crítica (< 0.40)'


    df['Estado_Salud'] = df['Sentimiento'].apply(clasificar_salud)
    salud_counts = df['Estado_Salud'].value_counts().reset_index()
    salud_counts.columns = ['Estado', 'Días']

    fig_pie = px.pie(
        salud_counts, values='Días', names='Estado', hole=0.5,
        color='Estado', color_discrete_map={
            'Óptima (>= 0.55)': '#10b981',
            'Estable (0.40 - 0.54)': '#94a3b8',
            'Crítica (< 0.40)': '#f43f5e'
        }
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False, height=350, template="plotly_white", margin=dict(l=10, r=20, t=10, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)



# --- 9. ANÁLISIS DE EVOLUCIÓN Y TENDENCIAS ---
st.write("---")
row3_1, row3_2 = st.columns([1, 1])

with row3_1:
    st.subheader("📈 Evolución Diaria (Desencadenantes)")

    # Filtramos solo los eventos de tipo Desencadenante
    df_des = df_events[df_events['Tipo'] == 'Desencadenante'].copy()

    if not df_des.empty and 'Fecha_Fin' in df_des.columns:
        # Extraemos un nombre corto para las pestañas (quitamos lo que hay entre paréntesis)
        tab_names = [evento.split('(')[0].strip() for evento in df_des['Evento']]

        # Creamos las pestañas interactivas de Streamlit
        tabs = st.tabs(tab_names)

        for i, row in df_des.reset_index().iterrows():
            with tabs[i]:
                # Filtramos el dataframe original para sacar todos los días de esta ventana
                mask = (df['Fecha'] >= row['Fecha']) & (df['Fecha'] <= row['Fecha_Fin'])
                df_window = df[mask]

                if not df_window.empty:
                    # Determinamos si la tendencia general fue subir o bajar para colorear la línea
                    sent_inicio = df_window.iloc[0]['Sentimiento']
                    sent_fin = df_window.iloc[-1]['Sentimiento']
                    color_linea = "#10b981" if sent_fin >= sent_inicio else "#f43f5e"

                    # Dibujamos la gráfica de línea día a día
                    fig_line = px.line(
                        df_window, x="Fecha", y="Sentimiento",
                        markers=True, hover_data={"Fecha": "|%d %b %Y", "Sentimiento": ":.3f"}
                    )

                    fig_line.update_traces(
                        line_color=color_linea,
                        line_width=3,
                        marker=dict(size=8, color='white', line=dict(width=2, color=color_linea))
                    )

                    # Ajustamos el rango del eje Y dinámicamente para que se vea bien el desnivel
                    y_min = df_window['Sentimiento'].min() - 0.05
                    y_max = df_window['Sentimiento'].max() + 0.05

                    fig_line.update_layout(
                        height=330, template="plotly_white", margin=dict(l=10, r=20, t=20, b=20),
                        xaxis=dict(title="", showgrid=False, tickformat="%d %b"),
                        yaxis=dict(title="<b>Sentimiento</b>", range=[y_min, y_max], gridcolor="#f1f5f9")
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.warning("Datos no disponibles para este periodo.")
    else:
        st.info("No hay eventos con Fecha_Fin configurada para mostrar esta gráfica.")

with row3_2:
    st.subheader("🎯 Volumen vs Sentimiento General")
    fig_scat = px.scatter(
        df, x="Volumen", y="Sentimiento", color="Sentimiento",
        color_continuous_scale="Viridis", trendline="lowess", trendline_color_override="#f43f5e"
    )
    fig_scat.update_layout(height=400, template="plotly_white", margin=dict(l=10, r=20, t=20, b=20))
    st.plotly_chart(fig_scat, use_container_width=True)

st.markdown(
    "<br><center><small>Validación de Datos v4.0 | Pipeline de Inteligencia Híbrida | Trabajo de Fin de Grado</small></center>",
    unsafe_allow_html=True)