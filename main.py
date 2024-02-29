import tkinter as tk
import ttkbootstrap as tb
from datetime import date
import sqlite3 as sql



root = tb.Window(themename="superhero")
root.resizable(width=False, height=False)
root.title("Control de Gastos")
root.geometry("400x300")

# Conexion a la base de datos
FILE = "database.db"
connection = sql.connect(FILE)
cursor = connection.cursor()




# Función Auxiliares 

# Eliminar todos los widgets en una ventana
def clear_window():
    for widget in root.winfo_children():
        widget.grid_forget()

# Reformar la ventana al tamaño estandar
def reshape():
    root.geometry("400x300")

# Label a mano para usar 
def temp():
    auxiliar.grid(row=3, columnspan=5)

def total_gastos(mes):
    meses = {"Enero":"01", "Febrero":"02", "Marzo":"03", "Abril":"04", "Mayo":"05", "Junio":"06", "Julio":"07", "Agosto":"08",
              "Septiembre":"09", "Octubre":"10", "Noviembre":"11", "Diciembre":"12"}
    # Data
    cursor.execute(f"SELECT importe, descripcion, strftime('%d', dia), strftime('%m', dia) as Mes FROM gastos WHERE Mes='{meses[mes]}';")
    datos = cursor.fetchall()
    # Calcular el total de los gastos
    total = 0
    for j in datos:
        total += j[0]
    total_2.configure(text=total)    


# Páginas principales
def menu_principal():
    clear_window()
    label.grid(row=0, columnspan=4, padx=10, pady=10)
    boton_ingresar.grid(row=1, column=1, padx=10, pady=10)
    boton_ver.grid(row =1, column =2, padx=10, pady=10)


def ingresar_gastos():
    clear_window()
    label_importe.grid(row=0, column=0, padx=10, pady=10)
    label_descripcion.grid(row=0, column=2, padx=10, pady=10)

    ingresar_importe.grid(row=1, column=0, padx=10, pady=10)
    ingresar_descripcion.grid(row=1, column=2, padx=10, pady=10)

    boton_submit_gasto.grid(row=2, column=1, padx=10, pady=20)

    boton_menu.grid(row=4, column=0, padx=10, pady=80)

    # Funcionalidad
    importe = ingresar_importe.get()
    descripcion = ingresar_descripcion.get()
    fecha = date.today()
    if len(importe) == 0:
        temp()
        auxiliar.configure(text="El importe no puede quedar vacio", bootstyle="inverse-danger")
    else:
        # Escribir a la base de datos
        cursor.execute("""INSERT INTO gastos ('importe', 'descripcion', 'dia') VALUES (:importe, :descripcion, :fecha);""",
                        {'importe':importe, 'descripcion':descripcion, 'fecha':fecha})
        
        # Guardar los cambios
        connection.commit()
        temp()
        auxiliar.configure(text="Datos ingresados correctamente", bootstyle="inverse-success")

    # Borra los datos del las entry widgets
    ingresar_importe.delete(0, "end")
    ingresar_descripcion.delete(0, "end")


def ver_gastos():
    clear_window()
    # Resize 
    root.geometry("700x500")

    # Data
    cursor.execute("SELECT importe, descripcion, dia FROM gastos")
    datos = cursor.fetchall()
    if len(datos) >= 10:
        size = 10
    else:
        size = len(datos)

    columns = ("importe", "descripcion", "dia")
    tree = tb.Treeview(root, bootstyle="success", columns=columns, show="headings", height=size)
    tree.heading("importe", text="Importe")
    tree.heading("descripcion", text="Descripcion del gasto")
    tree.heading("dia", text="Dia del gasto")


    for i in range(len(datos)):
        dato = datos.pop()
        tree.insert("", "end", values=dato)
    
        
    tree.grid(row=1, column=0, columnspan=4, padx=43)
    label_ultimos.grid(row=0, column=0, pady=5)
    menu_meses.grid(row=0, column=1, pady=5)
    menu_años.grid(row=0, column=2, pady=5)
    boton_menu.grid(row=2, column=0, pady=50)


def gastos_detalles(mes):
    clear_window()
    menu_meses.config(text=mes)
    meses = {"Enero":"01", "Febrero":"02", "Marzo":"03", "Abril":"04", "Mayo":"05", "Junio":"06", "Julio":"07", "Agosto":"08",
              "Septiembre":"09", "Octubre":"10", "Noviembre":"11", "Diciembre":"12"}
    today = date.today()
    year = today.year
    # Data
    cursor.execute(f"""SELECT importe, descripcion, strftime('%d', dia), strftime('%m', dia) as Mes,
                    strftime('%Y', dia) as Year FROM gastos WHERE Mes='{meses[mes]}' AND Year='{year}';""")
    datos = cursor.fetchall()
    if len(datos) >= 10:
        size = 10
    else:
        size = len(datos)

    columns = ("importe", "descripcion", "dia")
    tree = tb.Treeview(root, bootstyle="success", columns=columns, show="headings", height=size)
    tree.heading("importe", text="Importe")
    tree.heading("descripcion", text="Descripcion del gasto")
    tree.heading("dia", text="Dia del gasto")
    
    for i in range(len(datos)):
        dato = datos.pop()
        tree.insert("", "end", values=dato)
    



    tree.grid(row=1, column=0, columnspan=4, padx=43)
    label_ultimos.grid(row=0, column=0, pady=5)
    menu_meses.grid(row=0, column=1, pady=5)
    menu_años.grid(row=0, column=2, pady=5)
    frame.grid(row=3, column=0)
    total_1.grid(row=3, column=1)
    total_2.grid(row=3, column=2)
    boton_menu.grid(row=4, column=0, pady=10)


# Inicializar el menu principal
# Crear labels
label = tb.Label(text="Bienvenido!", font=("Times New Roman", 35), bootstyle="default")
# Poner las labels
label.grid(row=0, columnspan=3, padx=10, pady=10)
# Estilo de los botones
my_style = tb.Style()
my_style.configure("info.TButton", font=("Times New Roman", 15))
# Crear botones
boton_ingresar = tb.Button(text="Ingresar nuevo gasto", bootstyle="primary", style="info.TButton", command=ingresar_gastos)
boton_ver = tb.Button(text="Ver tus gastos", bootstyle="primary", style="info.TButton", command=ver_gastos)
# Poner los botones
boton_ingresar.grid(row=1, column=0, padx=10, pady=10)
boton_ver.grid(row =1, column =2, padx=10, pady=10)


# Boton de volver al menu principal
boton_menu = tb.Button(text="Volver al menu", bootstyle="secondary", command=lambda:[menu_principal(), reshape()])

# Pagina de ingresar nuevos gastos
label_importe = tb.Label(text="Importe:", font=("Times New Roman", 15))
label_descripcion = tb.Label(text="Descripcion:", font=("Times New Roman", 15))
ingresar_importe = tb.Entry(bootstyle="success", width=10)
ingresar_descripcion = tb.Entry(bootstyle="primary")
# Estilo de los botones
my_style_2 = tb.Style()
my_style_2.configure("primary.TButton", font=("Times New Roman", 10))
boton_submit_gasto = tb.Button(text="Ingresar", bootstyle="primary", style="primary.TButton", command=lambda:[ingresar_gastos(), temp()], width=10)

# Pagina de ver gastos
label_ultimos = tb.Label(text="Ultimos gastos", font=("Times New Roman", 20))
# Menu para elegir el mes
menu_meses = tb.Menubutton(root, bootstyle="primary", text="Mes", width=13)
inside_menu = tb.Menu(menu_meses)
item_var = tk.StringVar()
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
for x in meses:
    inside_menu.add_radiobutton(label=x, variable=item_var, command=lambda x=x: [gastos_detalles(x), total_gastos(x)])
menu_meses["menu"] = inside_menu

# Menu para elegir año (no funciona la eleccion del año)
today = date.today()
años = list(range(2023, today.year+1))
menu_años = tb.Menubutton(root, bootstyle="primary", text="Año", width=8)
inside_menu_años = tb.Menu(menu_años)
item_var_años = tk.StringVar()
for i in años:
    inside_menu_años.add_radiobutton(label=i, variable=item_var_años)
menu_años["menu"] = inside_menu_años

# Total de gasto por mes
frame = tb.LabelFrame(root, bootstyle="success")
total_1 = tb.Label(frame, text="Gastos totales:", font=("Times New Roman", 11)) 
total_2 = tb.Label(frame, text="", bootstyle="")


# Auxiliares
auxiliar = tb.Label()
separador = tb.Separator(bootstyle="primary")

# Mainloop
if __name__ == "__main__":
    root.mainloop()