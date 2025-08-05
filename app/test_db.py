import mysql.connector

db_config = {
    'host': '172.17.0.1',
    'user': 'hernan',
    'password': 'Cristiano8_', 
    'database': 'graxiano'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("✅ Conexión exitosa. Tablas:")
    for table in tables:
        print(f" - {table[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Error al conectar con MySQL:")
    print(e)

