import sqlite3 as sql

# Conexion a la base de datos
FILE = "database.db"


def get_gastos(FILE):

    connection = sql.connect(FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT importe, descripcion, dia FROM gastos")
    x = cursor.fetchall()

    return [x[i:i+10] for i in range(0, len(x), 10)]



print(len(get_gastos(FILE)))