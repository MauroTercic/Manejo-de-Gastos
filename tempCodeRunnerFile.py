    cursor.execute("""SELECT strftime('%d', '2035-12-01') AS "Day", strftime('%m', '2035-12-01') AS "Month", strftime('%Y', '2035-12-01') AS "Year" FROM gastos""")
    datos = cursor.fetchall()
