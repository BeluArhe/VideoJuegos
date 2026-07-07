import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta
import random

# --- 1. Configuración de la Base de Datos ---
conn = sqlite3.connect('data_warehouse.db')
cursor = conn.cursor()

# --- 2. Carga Batch (Inicial) de Dimensiones y Hechos ---

# 2.1. Cargar DimJuego (limpiando y estandarizando)
df_juegos = pd.read_csv('DimJuego.csv', encoding='utf-8')

# Limpieza básica: reemplazar NaN y estandarizar nombres de publishers
df_juegos['publisher'] = df_juegos['publisher'].fillna('Desconocido')
df_juegos['developer'] = df_juegos['developer'].fillna('Desconocido')

# Estandarización de publishers
publisher_map = {
    'Sony Computer Entertainment': 'Sony',
    'Sony Computer Entertainment America': 'Sony',
    'Sony Interactive Entertainment': 'Sony',
    'Microsoft Game Studios': 'Microsoft',
    'Microsoft Studios': 'Microsoft',
    'Electronic Arts': 'EA',
    'EA Sports': 'EA'
}
df_juegos['publisher'] = df_juegos['publisher'].replace(publisher_map)

# Guardar en la base de datos (Batch)
df_juegos.to_sql('DimJuego', conn, if_exists='replace', index=False)
print("✅ Batch: DimJuego cargada con", len(df_juegos), "registros.")

# 2.2. Generar y Cargar DimTiempo (2000-2024)
fechas = pd.date_range(start='2000-01-01', end='2024-12-31')
df_tiempo = pd.DataFrame({
    'ID_Tiempo': range(1, len(fechas) + 1),
    'Fecha': fechas,
    'Anio': fechas.year,
    'Mes': fechas.month,
    'Semana': fechas.isocalendar().week,
    'Dia': fechas.day,
    'Nombre_Mes': fechas.strftime('%B')
})
df_tiempo.to_sql('DimTiempo', conn, if_exists='replace', index=False)
print("✅ Batch: DimTiempo cargada con", len(df_tiempo), "registros.")

# 2.3. Generar y Cargar DimCliente (100 clientes)
clientes = []
for i in range(1, 101):
    paises = ['USA', 'MEX', 'CAN', 'UK', 'JPN', 'BRA']
    regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    clientes.append({
        'ID_Cliente': i,
        'Nombre': f'Cliente_{i}',
        'Pais': random.choice(paises),
        'Region': random.choice(regiones)
    })
df_clientes = pd.DataFrame(clientes)
df_clientes.to_sql('DimCliente', conn, if_exists='replace', index=False)
print("✅ Batch: DimCliente cargada con", len(df_clientes), "registros.")

# 2.4. Generar y Cargar Hecho_Ventas (10,000 registros históricos)
juegos_ids = df_juegos['id_juego'].tolist()
tiempos_ids = df_tiempo['ID_Tiempo'].tolist()
clientes_ids = df_clientes['ID_Cliente'].tolist()

ventas = []
for _ in range(10000):
    id_juego = random.choice(juegos_ids)
    id_tiempo = random.choice(tiempos_ids)
    id_cliente = random.choice(clientes_ids)
    cantidad = random.randint(1, 5)
    precio = round(random.uniform(19.99, 69.99), 2)
    total = round(cantidad * precio, 2)
    ventas.append([_, id_juego, id_tiempo, id_cliente, cantidad, precio, total])

df_ventas = pd.DataFrame(ventas, columns=['ID_Venta', 'ID_Juego', 'ID_Tiempo', 'ID_Cliente', 'Cantidad', 'Precio', 'Total'])
df_ventas.to_sql('Hecho_Ventas', conn, if_exists='replace', index=False)
print("✅ Batch: Hecho_Ventas cargada con", len(df_ventas), "registros.")

# --- 3. Carga Incremental (Simulación) ---
print("\n🔄 Iniciando carga incremental...")

# 3.1. Insertar nuevos juegos (simulando un nuevo batch)
nuevos_juegos = pd.DataFrame([
    {'nombre': 'Nuevo Juego 1', 'genero': 'Shooter', 'developer': 'Nuevo Dev', 'publisher': 'EA', 'id_juego': 9999},
    {'nombre': 'Nuevo Juego 2', 'genero': 'RPG', 'developer': 'Otro Dev', 'publisher': 'Sony', 'id_juego': 9998}
])

# Usar el flag de control: si existe, no insertar; si no existe, insertar
cursor.execute("SELECT COUNT(*) FROM DimJuego WHERE id_juego = 9999")
if cursor.fetchone()[0] == 0:
    nuevos_juegos.to_sql('DimJuego', conn, if_exists='append', index=False)
    print("✅ Incremental: 2 nuevos juegos añadidos a DimJuego.")

# 3.2. Insertar nuevas ventas (simulando un nuevo día)
nuevas_ventas = []
for _ in range(50):
    nuevas_ventas.append([10000 + _, random.choice(juegos_ids), random.choice(tiempos_ids), random.choice(clientes_ids), random.randint(1,3), round(random.uniform(19.99, 59.99),2), 0]) # Total calculado después

df_nuevas_ventas = pd.DataFrame(nuevas_ventas, columns=['ID_Venta', 'ID_Juego', 'ID_Tiempo', 'ID_Cliente', 'Cantidad', 'Precio', 'Total'])
df_nuevas_ventas['Total'] = df_nuevas_ventas['Cantidad'] * df_nuevas_ventas['Precio']

cursor.execute("SELECT MAX(ID_Venta) FROM Hecho_Ventas")
max_id = cursor.fetchone()[0] or 0
df_nuevas_ventas['ID_Venta'] = range(max_id + 1, max_id + 1 + len(df_nuevas_ventas))

df_nuevas_ventas.to_sql('Hecho_Ventas', conn, if_exists='append', index=False)
print("✅ Incremental: 50 nuevas ventas añadidas a Hecho_Ventas.")

# 4. Verificación del Orden de Carga (Dimensiones -> Hechos)
print("\n🔍 Verificando integridad referencial...")
cursor.execute("""
    SELECT COUNT(*) FROM Hecho_Ventas hv
    LEFT JOIN DimJuego dj ON hv.ID_Juego = dj.id_juego
    WHERE dj.id_juego IS NULL
""")
if cursor.fetchone()[0] == 0:
    print("✅ Integridad referencial OK: Todos los ID_Juego en Hecho_Ventas existen en DimJuego.")

cursor.execute("""
    SELECT COUNT(*) FROM Hecho_Ventas hv
    LEFT JOIN DimCliente dc ON hv.ID_Cliente = dc.ID_Cliente
    WHERE dc.ID_Cliente IS NULL
""")
if cursor.fetchone()[0] == 0:
    print("✅ Integridad referencial OK: Todos los ID_Cliente en Hecho_Ventas existen en DimCliente.")

conn.close()
print("\n🎯 Proceso de carga completado exitosamente.")