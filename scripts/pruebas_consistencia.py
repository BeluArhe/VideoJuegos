import sqlite3
import pandas as pd

conn = sqlite3.connect('data_warehouse.db')

# 1. Validar integridad referencial (IDs válidos)
print("🔍 Validación de Integridad Referencial...")
query = """
SELECT 
    (SELECT COUNT(*) FROM Hecho_Ventas hv LEFT JOIN DimJuego dj ON hv.ID_Juego = dj.id_juego WHERE dj.id_juego IS NULL) as Juegos_Invalidos,
    (SELECT COUNT(*) FROM Hecho_Ventas hv LEFT JOIN DimCliente dc ON hv.ID_Cliente = dc.ID_Cliente WHERE dc.ID_Cliente IS NULL) as Clientes_Invalidos,
    (SELECT COUNT(*) FROM Hecho_Ventas hv LEFT JOIN DimTiempo dt ON hv.ID_Tiempo = dt.ID_Tiempo WHERE dt.ID_Tiempo IS NULL) as Tiempo_Invalidos
"""
result = pd.read_sql(query, conn)
print(result)

# 2. Verificar formatos y unidades
print("\n🔍 Verificación de Formatos...")
# Precios no negativos
precios_negativos = pd.read_sql("SELECT COUNT(*) as Precios_Negativos FROM Hecho_Ventas WHERE Precio < 0", conn)
print(precios_negativos)
# Cantidades no negativas
cantidades_negativas = pd.read_sql("SELECT COUNT(*) as Cantidades_Negativas FROM Hecho_Ventas WHERE Cantidad < 0", conn)
print(cantidades_negativas)

# 3. Revisión de duplicados
print("\n🔍 Revisión de Duplicados...")
duplicados_dim = pd.read_sql("SELECT id_juego, COUNT(*) as count FROM DimJuego GROUP BY id_juego HAVING COUNT(*) > 1", conn)
print(f"Duplicados en DimJuego: {len(duplicados_dim)}")
duplicados_hechos = pd.read_sql("SELECT ID_Venta, COUNT(*) as count FROM Hecho_Ventas GROUP BY ID_Venta HAVING COUNT(*) > 1", conn)
print(f"Duplicados en Hecho_Ventas: {len(duplicados_hechos)}")

conn.close()