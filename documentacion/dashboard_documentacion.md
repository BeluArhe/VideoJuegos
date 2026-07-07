# 📊 Documentación del Dashboard de Ventas de Videojuegos

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación](#instalación)
5. [Cómo Ejecutar](#cómo-ejecutar)
6. [Componentes Principales](#componentes-principales)
7. [Filtros Interactivos](#filtros-interactivos)
8. [KPIs y Métricas](#kpis-y-métricas)
9. [Visualizaciones](#visualizaciones)
10. [Troubleshooting](#troubleshooting)
11. [Información Técnica](#información-técnica)

---

## 🎮 Descripción General

El Dashboard de Ventas de Videojuegos es una aplicación web interactiva construida con **Streamlit** que permite visualizar y analizar datos de ventas de videojuegos desde un Data Warehouse en SQLite.

Este dashboard proporciona un análisis integral de:
- Ventas totales y tendencias
- Rendimiento por género y publisher
- Análisis geográfico por región
- Comportamiento de clientes
- Comparativas y rankings de productos

**Fecha de creación:** 2024  
**Versión actual:** 1.0  
**Estado:** Producción

---

## ✨ Características

### Análisis de Ventas
- 📈 Seguimiento de ventas totales en tiempo real
- 📊 Tendencias mensuales y análisis temporal
- 🎯 Ventas segmentadas por múltiples dimensiones

### Filtros Inteligentes
- 📅 Filtro por rango de fechas personalizado
- 🎮 Filtro por género de videojuego
- 🏢 Filtro por casa productora (publisher)
- 🌍 Filtro por región geográfica

### Visualizaciones Interactivas
- Gráficos dinámicos con Plotly
- Tarjetas de métricas con valores destacados
- Tablas de datos con scroll horizontal
- Comparativas visuales

### Diseño Responsivo
- Interfaz moderna y atractiva
- Temas oscuro optimizado para legibilidad
- Distribución automática en columnas
- Compatible con dispositivos de diferentes tamaños

---

## 🔧 Requisitos Previos

Antes de instalar el dashboard, asegúrate de tener:

| Requisito | Versión Mínima | Notas |
|-----------|-----------------|-------|
| Python | 3.10+ | Recomendado: 3.11+ |
| pip | 20.0+ | Gestor de paquetes |
| SQLite | 3.0+ | Incluido en Python |
| Sistema Operativo | Windows, Linux, macOS | Compatible |

### Archivo Base de Datos
- **Ubicación:** `data_warehouse.db` (raíz del proyecto)
- **Formato:** SQLite3
- **Generación:** Ejecutar `scripts/carga_dw.py`

---

## 📦 Instalación

### Paso 1: Clonar o descargar el proyecto

```bash
cd ruta/del/proyecto/VideoJuegos
```

### Paso 2: Crear un entorno virtual (opcional pero recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r dashboard/requirements.txt
```

**Dependencias principales:**
```
streamlit>=1.28.0      # Framework web
pandas>=2.0.0          # Manipulación de datos
plotly>=5.18.0         # Visualizaciones interactivas
numpy>=1.24.0          # Operaciones numéricas
```

### Paso 4: Generar la Base de Datos (si no existe)

```bash
python scripts/carga_dw.py
```

Este script:
- ✅ Carga dimensión de juegos
- ✅ Genera tabla de tiempo (2000-2024)
- ✅ Genera tabla de clientes (100 registros)
- ✅ Crea tabla de hechos de ventas (10,000 registros)
- ✅ Valida integridad referencial

---

## 🚀 Cómo Ejecutar

### Opción 1: Desde Terminal (Recomendado)

```bash
streamlit run dashboard/dashboard_dw.py
```

### Opción 2: Usando Script de Lanzamiento (Windows)

```bash
cd dashboard
run_dashboard.bat
```

**Salida esperada:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Acceder al Dashboard

Abre en tu navegador web:
- 🔗 [http://localhost:8501](http://localhost:8501)

### Detener el Dashboard

Presiona `Ctrl + C` en la terminal para detener la aplicación.

---

## 🎯 Componentes Principales

### Header Principal
```
🎮 Data Warehouse - Dashboard de Ventas de Videojuegos
```
Encabezado con gradiente personalizado que identifica la aplicación.

### Panel Lateral de Filtros
Ubicado en la izquierda de la pantalla, contiene todos los controles de filtrado:

#### 📅 Rango de Fechas
- Selector dual de fechas inicio y fin
- Rango disponible: 2000-2024
- Recalcula automáticamente todos los KPIs

#### 🎮 Géneros
- Dropdown con lista de géneros únicos
- Opción "Todos" para mostrar todos los géneros
- Actualiza visualizaciones en tiempo real

#### 🏢 Publishers
- Selector de casa productora
- Incluye opción "Todos"
- Filtra datos por empresa desarrolladora

#### 🌍 Región
- Selector geográfico
- Opciones: Todas, y regiones individuales
- Permite análisis geográfico específico

---

## 🔍 Filtros Interactivos

### Funcionamiento de Filtros

1. **Filtro de Fecha**
   - Selecciona un rango: fecha inicio → fecha fin
   - Afecta: Todos los gráficos, KPIs y tablas
   - Reinicia automáticamente

2. **Filtros Categóricos**
   - Selecciona un valor del dropdown
   - Se aplica inmediatamente
   - Se pueden combinar múltiples filtros

3. **Aplicación en Cascada**
   - Los filtros se aplican secuencialmente
   - Cada filtro reduce el conjunto de datos
   - Afecta a todos los elementos visuales

### Ejemplo de Uso

Para analizar ventas de juegos de acción en NA durante 2023:

1. Abre el sidebar (si está colapsado)
2. Establece rango: 01/01/2023 → 31/12/2023
3. Selecciona "Acción" en Géneros
4. Selecciona "NA" en Región
5. Observa cómo se actualizan todos los gráficos

---

## 📊 KPIs y Métricas

### KPIs Principales (Primera Fila)

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| 💰 Ventas Totales | Suma de todos los totales de venta | `SUM(Total)` |
| 📦 Transacciones | Cantidad total de transacciones | `COUNT(*)` |
| 👥 Clientes Únicos | Cantidad de clientes diferentes | `COUNT(DISTINCT ID_Cliente)` |
| 🎮 Juegos Vendidos | Cantidad de juegos únicos | `COUNT(DISTINCT ID_Juego)` |
| 🎫 Ticket Promedio | Venta promedio por transacción | `AVG(Total)` |

### KPIs Derivados

- **Ventas por Día:** `Total Ventas / Días en Rango`
- **Venta Máxima:** Transacción de mayor valor
- **Venta Mínima:** Transacción de menor valor

---

## 📈 Visualizaciones

### 1. Gráficos de Series Temporales
**Tipo:** Línea interactiva con Plotly  
**Datos:** Ventas acumuladas por mes  
**Uso:** Identificar tendencias y estacionalidad

### 2. Gráficos de Barras (Top Productos)
**Tipo:** Barra horizontal  
**Datos:** Top 10 videojuegos por ventas  
**Interactividad:** Hover para valores exactos

### 3. Gráficos de Distribución (Género)
**Tipo:** Pie chart / Donut  
**Datos:** Proporción de ventas por género  
**Acción:** Click para filtrar (si está disponible)

### 4. Gráficos Geográficos (Región)
**Tipo:** Barra agrupada  
**Datos:** Ventas por región y período  
**Análisis:** Comparativa regional

### 5. Tablas de Datos
**Tipo:** Dataframe interactivo  
**Columnas:** ID_Juego, Nombre, Ventas, Precio, Género  
**Funciones:** Scroll, ordenamiento, búsqueda

---

## 🆘 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'streamlit'"

**Solución:**
```bash
pip install streamlit
# o instalar todas las dependencias
pip install -r dashboard/requirements.txt
```

### Problema: "FileNotFoundError: data_warehouse.db"

**Causa:** La base de datos no ha sido generada.

**Solución:**
```bash
# Generar la BD desde cero
python scripts/carga_dw.py
```

### Problema: Dashboard carga lentamente

**Posibles causas y soluciones:**
- ❌ Base de datos grande → Reduce rango de fechas
- ❌ Conexión lenta → Verifica conexión a red
- ❌ Cache vacío → Primera carga es más lenta (normal)

**Nota:** El dashboard cachea datos por 5 minutos después de la carga inicial.

### Problema: Puerto 8501 ya está en uso

**Solución:**
```bash
streamlit run dashboard/dashboard_dw.py --server.port 8502
```

### Problema: Los filtros no funcionan

**Verificar:**
1. ¿Los datos están cargados? (Verifica `data_warehouse.db`)
2. ¿Hay datos en el rango de fechas? (Expande el rango)
3. ¿El valor existe en los datos? (Reinicia el filtro)

---

## 💻 Información Técnica

### Arquitectura

```
Dashboard (Streamlit)
    ↓
Conexión SQLite
    ↓
Data Warehouse (data_warehouse.db)
    ├── DimJuego (Dimensión)
    ├── DimTiempo (Dimensión)
    ├── DimCliente (Dimensión)
    ├── DimPlataforma (Dimensión)
    ├── DimRatingCritico (Dimensión)
    └── Hecho_Ventas (Tabla de Hechos)
```

### Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|------------|---------|
| Backend | Python | 3.10+ |
| Framework Web | Streamlit | 1.28.0+ |
| Base de Datos | SQLite3 | 3.0+ |
| Análisis de Datos | Pandas | 2.0.0+ |
| Visualización | Plotly | 5.18.0+ |
| Cálculos | NumPy | 1.24.0+ |

### Estructura de Archivos del Dashboard

```
dashboard/
├── dashboard_dw.py          # Script principal de Streamlit
├── requirements.txt         # Dependencias Python
└── run_dashboard.bat       # Lanzador Windows
```

### Conexión a Base de Datos

**Ubicación:** `../data_warehouse.db` (relativa al script)

**Método:** SQLite3 con conexión persistente  
**Cache:** 5 minutos TTL  
**Modo:** Lectura (read-only recomendado)

### Flujo de Datos

1. **Carga:** Lee datos de 4 tablas y fusiona mediante JOINs
2. **Transformación:** Convierte fechas, crea columnas derivadas
3. **Filtrado:** Aplica filtros del sidebar
4. **Agregación:** Calcula KPIs y métricas
5. **Visualización:** Renderiza gráficos con Plotly

### Optimizaciones Implementadas

- ✅ `@st.cache_resource` para conexión persistente
- ✅ `@st.cache_data` para caché de datos (TTL 5 min)
- ✅ Cálculos vectorizados con Pandas/NumPy
- ✅ Carga condicional de datos (solo filtros aplicados)
- ✅ Plotly para gráficos interactivos sin recarga

---

## 📝 Notas Importantes

### Validación de Datos
- Los datos se validan en `scripts/pruebas_consistencia.py`
- Integridad referencial verificada automáticamente
- Log de validación: `documentacion/logs/pruebas_consistencia.log`

### Cálculo de KPIs
- KPIs principales calculados en `scripts/kpis_validacion.py`
- Se recalculan según filtros aplicados
- Log de KPIs: `documentacion/logs/kpis_validacion.log`

### Performance
- Para datasets > 1M registros: Considera particionar datos
- Índices recomendados en columnas de filtrado
- Considerar Data Warehouse agregado para grandes volúmenes

### Actualización de Datos
Para agregar nuevos datos:
1. Actualizar archivos CSV fuente
2. Ejecutar `scripts/carga_dw.py` (carga incremental)
3. Reiniciar dashboard (Ctrl+C y reiniciar)

---

## 📞 Soporte y Contacto

**Proyecto:** BI3006 - Data Warehouse y Dashboard de Ventas  
**Semestre:** 7mo Semestre  
**Institución:** BI - Business Intelligence  

**Para reportar problemas:**
1. Verifica los logs: `documentacion/logs/`
2. Revisa la sección [Troubleshooting](#troubleshooting)
3. Valida la base de datos: `python scripts/pruebas_consistencia.py`

---

**Última actualización:** 2024  
**Versión de documentación:** 1.0
