import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

# --- Configuración de la página ---
st.set_page_config(
    page_title="Data Warehouse - Dashboard de Ventas de Videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS personalizados ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .filter-section {
        background: #1e1e2e;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Conexión a la base de datos ---
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'data_warehouse.db'

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_data():
    conn = get_connection()
    
    # Cargar datos de las tablas
    df_ventas = pd.read_sql("SELECT * FROM Hecho_Ventas", conn)
    df_juegos = pd.read_sql("SELECT * FROM DimJuego", conn)
    df_tiempo = pd.read_sql("SELECT * FROM DimTiempo", conn)
    df_clientes = pd.read_sql("SELECT * FROM DimCliente", conn)
    
    # Unir tablas para análisis
    df_full = df_ventas.merge(df_juegos, left_on='ID_Juego', right_on='id_juego')
    df_full = df_full.merge(df_tiempo, on='ID_Tiempo')
    df_full = df_full.merge(df_clientes, on='ID_Cliente')
    
    # Agregar columnas derivadas
    df_full['Fecha_DT'] = pd.to_datetime(df_full['Fecha'])
    df_full['Año_Mes'] = df_full['Fecha_DT'].dt.strftime('%Y-%m')
    df_full['Día_Semana'] = df_full['Fecha_DT'].dt.day_name()
    
    return df_full, df_juegos, df_tiempo, df_clientes

# --- Cargar datos ---
with st.spinner('Cargando datos del Data Warehouse...'):
    df_full, df_juegos, df_tiempo, df_clientes = load_data()

# --- Barra lateral de filtros ---
st.sidebar.markdown("## 🎯 Filtros Interactivos")

# Filtro de fecha
st.sidebar.markdown("### 📅 Rango de Fechas")
min_date = df_full['Fecha_DT'].min().date()
max_date = df_full['Fecha_DT'].max().date()

date_range = st.sidebar.date_input(
    "Seleccionar período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_full[
        (df_full['Fecha_DT'].dt.date >= start_date) &
        (df_full['Fecha_DT'].dt.date <= end_date)
    ]
else:
    df_filtered = df_full

# Filtro de género
st.sidebar.markdown("### 🎮 Géneros")
generos = ['Todos'] + sorted(df_full['genero'].unique().tolist())
genero_selected = st.sidebar.selectbox("Filtrar por género", generos)
if genero_selected != 'Todos':
    df_filtered = df_filtered[df_filtered['genero'] == genero_selected]

# Filtro de publisher
st.sidebar.markdown("### 🏢 Publishers")
publishers = ['Todos'] + sorted(df_full['publisher'].unique().tolist())
publisher_selected = st.sidebar.selectbox("Filtrar por publisher", publishers)
if publisher_selected != 'Todos':
    df_filtered = df_filtered[df_filtered['publisher'] == publisher_selected]

# Filtro de región
st.sidebar.markdown("### 🌍 Región")
regiones = ['Todas'] + sorted(df_full['Region'].unique().tolist())
region_selected = st.sidebar.selectbox("Filtrar por región", regiones)
if region_selected != 'Todas':
    df_filtered = df_filtered[df_filtered['Region'] == region_selected]

# --- KPIs Principales ---
st.markdown('<div class="main-header">🎮 Data Warehouse - Dashboard de Ventas</div>', unsafe_allow_html=True)

# Calcular KPIs
total_ventas = df_filtered['Total'].sum()
total_transacciones = len(df_filtered)
total_clientes = df_filtered['ID_Cliente'].nunique()
total_juegos = df_filtered['ID_Juego'].nunique()
ticket_promedio = df_filtered['Total'].mean()
ventas_por_dia = total_transacciones / max(1, (end_date - start_date).days)

# Mostrar KPIs en fila
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Ventas Totales",
        value=f"${total_ventas:,.2f}",
        delta=f"${total_ventas/1000:.1f}K"
    )

with col2:
    st.metric(
        label="🛒 Transacciones",
        value=f"{total_transacciones:,}",
        delta=f"{ventas_por_dia:.0f}/día"
    )

with col3:
    st.metric(
        label="👥 Clientes",
        value=f"{total_clientes:,}"
    )

with col4:
    st.metric(
        label="🎮 Juegos Vendidos",
        value=f"{total_juegos:,}"
    )

with col5:
    st.metric(
        label="💳 Ticket Promedio",
        value=f"${ticket_promedio:,.2f}"
    )

st.markdown("---")

# --- Gráficos Interactivos ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Ventas por Tiempo",
    "🎮 Top Juegos",
    "🌍 Distribución Geográfica",
    "🏢 Análisis por Publisher",
    "📊 Detalle de Datos"
])

# Tab 1: Ventas por Tiempo
with tab1:
    st.markdown("### 📈 Evolución de Ventas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ventas por mes
        ventas_mes = df_filtered.groupby('Año_Mes')['Total'].sum().reset_index()
        ventas_mes = ventas_mes.sort_values('Año_Mes')
        
        fig_mes = px.line(
            ventas_mes,
            x='Año_Mes',
            y='Total',
            title='Ventas Mensuales',
            labels={'Año_Mes': 'Mes', 'Total': 'Ventas ($)'}
        )
        fig_mes.update_layout(
            xaxis_tickangle=-45,
            height=400,
            template='plotly_dark'
        )
        st.plotly_chart(fig_mes, use_container_width=True)
    
    with col2:
        # Ventas por día de la semana
        ventas_dia = df_filtered.groupby('Día_Semana')['Total'].sum().reset_index()
        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ventas_dia['Día_Semana'] = pd.Categorical(ventas_dia['Día_Semana'], categories=orden_dias, ordered=True)
        ventas_dia = ventas_dia.sort_values('Día_Semana')
        
        fig_dia = px.bar(
            ventas_dia,
            x='Día_Semana',
            y='Total',
            title='Ventas por Día de la Semana',
            labels={'Día_Semana': 'Día', 'Total': 'Ventas ($)'},
            color='Total',
            color_continuous_scale='Viridis'
        )
        fig_dia.update_layout(
            height=400,
            template='plotly_dark'
        )
        st.plotly_chart(fig_dia, use_container_width=True)
    
    # Ventas por año
    ventas_anio = df_filtered.groupby('Anio')['Total'].sum().reset_index()
    fig_anio = px.bar(
        ventas_anio,
        x='Anio',
        y='Total',
        title='Ventas por Año',
        labels={'Anio': 'Año', 'Total': 'Ventas ($)'},
        color='Total',
        color_continuous_scale='Plasma'
    )
    fig_anio.update_layout(height=400, template='plotly_dark')
    st.plotly_chart(fig_anio, use_container_width=True)

# Tab 2: Top Juegos
with tab2:
    st.markdown("### 🎮 Top Juegos Más Vendidos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top juegos por cantidad
        top_juegos = df_filtered.groupby('nombre')['Cantidad'].sum().reset_index()
        top_juegos = top_juegos.sort_values('Cantidad', ascending=False).head(10)
        
        fig_top = px.bar(
            top_juegos,
            x='Cantidad',
            y='nombre',
            orientation='h',
            title='Top 10 Juegos por Cantidad Vendida',
            labels={'Cantidad': 'Unidades Vendidas', 'nombre': 'Juego'},
            color='Cantidad',
            color_continuous_scale='Inferno'
        )
        fig_top.update_layout(height=500, template='plotly_dark')
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Top juegos por ingresos
        top_ingresos = df_filtered.groupby('nombre')['Total'].sum().reset_index()
        top_ingresos = top_ingresos.sort_values('Total', ascending=False).head(10)
        
        fig_top_ingresos = px.bar(
            top_ingresos,
            x='Total',
            y='nombre',
            orientation='h',
            title='Top 10 Juegos por Ingresos',
            labels={'Total': 'Ingresos ($)', 'nombre': 'Juego'},
            color='Total',
            color_continuous_scale='Magma'
        )
        fig_top_ingresos.update_layout(height=500, template='plotly_dark')
        st.plotly_chart(fig_top_ingresos, use_container_width=True)

# Tab 3: Distribución Geográfica
with tab3:
    st.markdown("### 🌍 Distribución Geográfica de Ventas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ventas por país
        ventas_pais = df_filtered.groupby('Pais')['Total'].sum().reset_index()
        ventas_pais = ventas_pais.sort_values('Total', ascending=False)
        
        fig_pais = px.pie(
            ventas_pais,
            values='Total',
            names='Pais',
            title='Distribución de Ventas por País',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_pais.update_layout(height=450, template='plotly_dark')
        st.plotly_chart(fig_pais, use_container_width=True)
    
    with col2:
        # Ventas por región
        ventas_region = df_filtered.groupby('Region')['Total'].sum().reset_index()
        
        fig_region = px.bar(
            ventas_region,
            x='Region',
            y='Total',
            title='Ventas por Región',
            labels={'Region': 'Región', 'Total': 'Ventas ($)'},
            color='Total',
            color_continuous_scale='Turbo'
        )
        fig_region.update_layout(height=450, template='plotly_dark')
        st.plotly_chart(fig_region, use_container_width=True)

    st.markdown("#### 🌎 Mapa Mundial de Ventas")
    pais_to_iso3 = {
        'UK': 'GBR',
        'CAN': 'CAN',
        'BRA': 'BRA',
        'USA': 'USA',
        'MEX': 'MEX',
        'JPN': 'JPN'
    }

    ventas_mundo = df_filtered.groupby('Pais')['Total'].sum().reset_index()
    ventas_mundo['ISO3'] = ventas_mundo['Pais'].map(pais_to_iso3)
    ventas_mundo = ventas_mundo.dropna(subset=['ISO3'])

    if not ventas_mundo.empty:
        fig_mundo = px.choropleth(
            ventas_mundo,
            locations='ISO3',
            color='Total',
            hover_name='Pais',
            color_continuous_scale='YlOrRd',
            title='Ventas por País en el Mapa Mundial'
        )
        fig_mundo.update_geos(projection_type='natural earth', showcoastlines=True, showland=True)
        fig_mundo.update_layout(height=550, template='plotly_dark')
        st.plotly_chart(fig_mundo, use_container_width=True)
    else:
        st.info("No hay países válidos para mostrar en el mapa mundial con el filtro actual.")
    
    # Mapa de calor de clientes
    st.markdown("#### 🗺️ Distribución de Clientes por País y Región")
    heatmap_data = df_filtered.groupby(['Pais', 'Region']).size().reset_index(name='Clientes')
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x='Pais',
        y='Region',
        z='Clientes',
        title='Mapa de Calor: Clientes por País y Región',
        color_continuous_scale='Viridis'
    )
    fig_heatmap.update_layout(height=400, template='plotly_dark')
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Tab 4: Análisis por Publisher
with tab4:
    st.markdown("### 🏢 Análisis por Publisher")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ventas por publisher
        ventas_publisher = df_filtered.groupby('publisher')['Total'].sum().reset_index()
        ventas_publisher = ventas_publisher.sort_values('Total', ascending=False).head(10)
        
        fig_publisher = px.bar(
            ventas_publisher,
            x='publisher',
            y='Total',
            title='Top 10 Publishers por Ingresos',
            labels={'publisher': 'Publisher', 'Total': 'Ingresos ($)'},
            color='Total',
            color_continuous_scale='Cividis'
        )
        fig_publisher.update_layout(height=450, template='plotly_dark')
        st.plotly_chart(fig_publisher, use_container_width=True)
    
    with col2:
        # Cantidad de juegos por publisher
        juegos_publisher = df_filtered.groupby('publisher')['ID_Juego'].nunique().reset_index()
        juegos_publisher = juegos_publisher.sort_values('ID_Juego', ascending=False).head(10)
        
        fig_juegos_pub = px.bar(
            juegos_publisher,
            x='publisher',
            y='ID_Juego',
            title='Top 10 Publishers por Cantidad de Juegos',
            labels={'publisher': 'Publisher', 'ID_Juego': 'Número de Juegos'},
            color='ID_Juego',
            color_continuous_scale='Viridis'
        )
        fig_juegos_pub.update_layout(height=450, template='plotly_dark')
        st.plotly_chart(fig_juegos_pub, use_container_width=True)
    
    # Análisis de género por publisher
    st.markdown("#### 📊 Géneros Populares por Publisher")
    
    # Seleccionar publishers para comparar
    top_publishers = ventas_publisher['publisher'].head(5).tolist()
    selected_publishers = st.multiselect(
        "Seleccionar Publishers para comparar",
        options=sorted(df_filtered['publisher'].unique()),
        default=top_publishers
    )
    
    if selected_publishers:
        genre_publisher = df_filtered[df_filtered['publisher'].isin(selected_publishers)]
        genre_publisher = genre_publisher.groupby(['publisher', 'genero'])['Total'].sum().reset_index()
        
        fig_genre_pub = px.bar(
            genre_publisher,
            x='publisher',
            y='Total',
            color='genero',
            title='Distribución de Géneros por Publisher',
            labels={'publisher': 'Publisher', 'Total': 'Ingresos ($)', 'genero': 'Género'},
            barmode='group'
        )
        fig_genre_pub.update_layout(height=450, template='plotly_dark')
        st.plotly_chart(fig_genre_pub, use_container_width=True)

# Tab 5: Datos Detallados
with tab5:
    st.markdown("### 📊 Datos Detallados")
    
    # Selector de visualización
    view_type = st.radio(
        "Seleccionar vista:",
        ['Ventas Detalladas', 'Resumen por Juego', 'Resumen por Cliente'],
        horizontal=True
    )
    
    if view_type == 'Ventas Detalladas':
        st.dataframe(
            df_filtered[['ID_Venta', 'nombre', 'genero', 'Fecha', 'Cantidad', 'Precio', 'Total', 'Pais', 'Region']],
            use_container_width=True,
            height=400
        )
        
        # Botón de descarga
        csv = df_filtered[['ID_Venta', 'nombre', 'genero', 'Fecha', 'Cantidad', 'Precio', 'Total', 'Pais', 'Region']].to_csv(index=False)
        st.download_button(
            label="📥 Descargar datos en CSV",
            data=csv,
            file_name=f"ventas_filtradas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif view_type == 'Resumen por Juego':
        resumen_juego = df_filtered.groupby(['nombre', 'genero']).agg({
            'Cantidad': 'sum',
            'Total': 'sum',
            'ID_Venta': 'count'
        }).reset_index()
        resumen_juego.columns = ['Juego', 'Género', 'Unidades Vendidas', 'Ingresos Totales', 'Número de Transacciones']
        st.dataframe(resumen_juego, use_container_width=True, height=400)
    
    else:  # Resumen por Cliente
        resumen_cliente = df_filtered.groupby(['ID_Cliente', 'Pais', 'Region']).agg({
            'Total': 'sum',
            'ID_Venta': 'count'
        }).reset_index()
        resumen_cliente.columns = ['ID Cliente', 'País', 'Región', 'Gasto Total', 'Compras']
        st.dataframe(resumen_cliente, use_container_width=True, height=400)

# --- Pie de página ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 1rem;'>
        🎮 Data Warehouse de Ventas de Videojuegos | 
        Datos actualizados: {} | 
        Registros cargados: {:,}
    </div>
    """.format(
        datetime.now().strftime('%Y-%m-%d %H:%M'),
        len(df_filtered)
    ),
    unsafe_allow_html=True
)