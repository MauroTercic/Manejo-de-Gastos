import sqlite3 as sql
from datetime import date
# Conexion a la base de datos
FILE = "database.db"

connection = sql.connect(FILE)
cursor = connection.cursor()

def get_gastos(FILE):


    cursor.execute("SELECT importe, descripcion, dia FROM gastos")
    x = cursor.fetchall()

    return [x[i:i+10] for i in range(0, len(x), 10)]



# Para elegir todo, pero ahora solo necesito el mes. Lo dejo comentando por las dudas
#cursor.execute("""SELECT strftime('%d', dia) AS "Day", strftime('%m', dia) AS "Month", strftime('%Y', dia) AS "Year" FROM gastos""")
#datos = cursor.fetchall()
#print(datos)


def t(x,y):
    meses = {"Enero":"01", "Febrero":"02", "Marzo":"01", "Abril":"01", "Mayo":"01", "Junio":"01", "Julio":"01", "Agosto":"01",
              "Septiembre":"01", "Octubre":"01", "Noviembre":"01", "Diciembre":"01"}
    
    # Data
    cursor.execute(f"""SELECT importe, descripcion, strftime('%d', dia),
                    strftime('%m', dia) as Mes, strftime('%Y', dia) as Año FROM gastos WHERE Mes='{meses[x]}' AND Año='{y}';""")
    datos = cursor.fetchall()
    print(datos)


#t("Febrero", '2024')


today = date.today()
años = list(range(2023, today.year+1))

for i in años:
    print(i)