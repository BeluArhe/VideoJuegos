import sqlite3
import pandas as pd

conn = sqlite3.connect('data_warehouse.db')

print("📊 Calculando KPIs...")

# 1. Ventas por mes
query_ventas_mes = """
SELECT 
    dt.Anio,
    dt.Nombre_Mes,
    SUM(hv.Total) as Ventas_Totales
FROM Hecho_Ventas hv
JOIN DimTiempo dt ON hv.ID_Tiempo = dt.ID_Tiempo
GROUP BY dt.Anio, dt.Mes
ORDER BY dt.Anio, dt.Mes
LIMIT 12
"""
ventas_mes = pd.read_sql(query_ventas_mes, conn)
print("\n📅 Ventas por mes (últimos 12 meses):")
print(ventas_mes)

# 2. Clientes activos por región
query_clientes_region = """
SELECT 
    dc.Region,
    COUNT(DISTINCT hv.ID_Cliente) as Clientes_Activos
FROM Hecho_Ventas hv
JOIN DimCliente dc ON hv.ID_Cliente = dc.ID_Cliente
GROUP BY dc.Region
ORDER BY Clientes_Activos DESC
"""
clientes_region = pd.read_sql(query_clientes_region, conn)
print("\n🌍 Clientes activos por región:")
print(clientes_region)

# 3. Total de productos vendidos (top 10)
query_top_productos = """
SELECT 
    dj.nombre as Juego,
    SUM(hv.Cantidad) as Total_Vendido
FROM Hecho_Ventas hv
JOIN DimJuego dj ON hv.ID_Juego = dj.id_juego
GROUP BY hv.ID_Juego
ORDER BY Total_Vendido DESC
LIMIT 10
"""
top_productos = pd.read_sql(query_top_productos, conn)
print("\n🎮 Top 10 productos más vendidos:")
print(top_productos)

# 4. Ticket promedio por cliente
query_ticket_promedio = """
SELECT 
    AVG(Total) as Ticket_Promedio
FROM Hecho_Ventas
"""
ticket_promedio = pd.read_sql(query_ticket_promedio, conn)
print(f"\n💰 Ticket promedio por cliente: ${ticket_promedio.iloc[0, 0]:.2f}")

# 5. Comparación con datos fuente (simulada)
print("\n📊 Comparación con datos fuente:")
print("Total de juegos en catálogo:", pd.read_sql("SELECT COUNT(*) FROM DimJuego", conn).iloc[0, 0])
print("Total de ventas registradas:", pd.read_sql("SELECT COUNT(*) FROM Hecho_Ventas", conn).iloc[0, 0])
print("Total de clientes:", pd.read_sql("SELECT COUNT(*) FROM DimCliente", conn).iloc[0, 0])

conn.close()