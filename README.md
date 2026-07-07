# BI3006 - Data Warehouse y Dashboard de Ventas

Proyecto de ejemplo para construir un Data Warehouse en SQLite, ejecutar validaciones de consistencia y visualizar KPIs en un dashboard interactivo con Streamlit.

## 1. Estructura del proyecto

```text
Coronado.Quizhpe.Raura.Zuñiga.DW/
├── dashboard/
│   ├── dashboard_dw.py
│   └── requirements.txt
├── documentacion/
│   ├── bitacora_carga.txt
│   └── logs/
├── scripts/
│   ├── carga_dw.py
│   ├── pruebas_consistencia.py
│   └── kpis_validacion.py
├── DimJuego.csv
├── DimPlataforma.csv
├── DimRatingCritico.csv
├── DimTiempo.csv
├── FactVentas.csv
└── data_warehouse.db
```

## 2. Requisitos

- Python 3.10+
- pip
- Windows, Linux o macOS

## 3. Instalación de dependencias

Desde la raiz del proyecto:

```bash
pip install -r dashboard/requirements.txt
```

Nota:
- No agregues sqlite3 al archivo de requirements. sqlite3 ya viene en la libreria estandar de Python.

## 4. Ejecucion paso a paso

Ejecuta estos comandos en orden desde la raiz del proyecto.

### Paso 1: Cargar el Data Warehouse

```bash
python scripts/carga_dw.py
```

Que hace este script:
- Carga la dimension de juegos desde DimJuego.csv
- Genera DimTiempo (2000-2024)
- Genera DimCliente (100 clientes)
- Genera Hecho_Ventas (10000 registros)
- Simula carga incremental de ventas
- Verifica integridad referencial basica

### Paso 2: Ejecutar pruebas de consistencia

```bash
python scripts/pruebas_consistencia.py
```

Valida:
- Integridad referencial entre hechos y dimensiones
- Precios y cantidades no negativas
- Duplicados en claves de negocio

Los logs completos de esta corrida se guardan en `documentacion/logs/pruebas_consistencia.log`.

### Paso 3: Calcular y validar KPIs

```bash
python scripts/kpis_validacion.py
```

Calcula:
- Ventas por mes
- Clientes activos por region
- Top productos vendidos
- Ticket promedio
- Conteos generales de tablas

Los logs completos de esta corrida se guardan en `documentacion/logs/kpis_validacion.log`.

### Paso 4: Iniciar dashboard

```bash
streamlit run dashboard/dashboard_dw.py
```

Luego abre en navegador:
- http://localhost:8501

El arranque del dashboard también deja evidencia en `documentacion/logs/dashboard.log`.

## 5. Bitácora y logs

La evidencia principal de la ejecución queda en `documentacion/bitacora_carga.txt`. Ese archivo resume la corrida con marcas de tiempo, duración, verificaciones y una referencia a los logs completos.

Los archivos separados de evidencia están en:

- `documentacion/logs/carga_dw.log`
- `documentacion/logs/pruebas_consistencia.log`
- `documentacion/logs/kpis_validacion.log`
- `documentacion/logs/dashboard.log`

## 6. Flujo recomendado de trabajo

```text
Instalar dependencias -> Cargar DW -> Probar consistencia -> Validar KPIs -> Abrir dashboard
```

## 7. Solución de problemas

### Error: No such file or directory: DimJuego.csv

Causa:
- El script busca DimJuego.csv en la raiz del proyecto.

Solucion:
- Verifica que el archivo exista en la raiz con ese nombre exacto.
- Los CSV fuente ya deben estar en la raiz del proyecto con esos nombres.

### Error al iniciar Streamlit por puerto ocupado

Prueba:

```bash
streamlit run dashboard/dashboard_dw.py --server.port 8502
```

### Reiniciar la base y volver a cargar

Si quieres regenerar todo desde cero, elimina data_warehouse.db y vuelve a ejecutar:

```bash
python scripts/carga_dw.py
```

## 8. Resultado esperado

Al finalizar el flujo completo:
- Base SQLite data_warehouse.db creada y poblada
- Validaciones de consistencia en cero errores
- KPIs impresos en consola
- Dashboard interactivo disponible en localhost
