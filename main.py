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

def tree():
    pass

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
        x = 10
    else:
        x = len(datos)
    columns = ("importe", "descripcion", "dia")
    tree = tb.Treeview(root, bootstyle="success", columns=columns, show="headings", height=x)
    tree.heading("importe", text="Importe")
    tree.heading("descripcion", text="Descripcion del gasto")
    tree.heading("dia", text="Dia del gasto")


    for i in range(len(datos)):
        dato = datos.pop()
        tree.insert("", "end", values=dato)
    
        
    tree.grid(row=1, column=0, columnspan=4, padx=43)
    label_ultimos.grid(row=0, column=1, pady=5)
    menu.grid(row=0, column=2, pady=5)
    boton_menu.grid(row=2, column=0, pady=10)

def gastos_meses(x):
    menu.config(text=x)
    meses = {"Enero":"01", "Febrero":"02", "Marzo":"01", "Abril":"01", "Mayo":"01", "Junio":"01", "Julio":"01", "Agosto":"01",
              "Septiembre":"01", "Octubre":"01", "Noviembre":"01", "Diciembre":"01"}
    
    # Data
    cursor.execute(f"SELECT strftime('%m', dia) as Mes, importe, descripcion FROM gastos WHERE Mes='{meses[x]}';")
    datos = cursor.fetchall()


    


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
menu = tb.Menubutton(root, bootstyle="primary", text="Meses", width=13)
inside_menu = tb.Menu(menu)

item_var = tk.StringVar()
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
for i in meses:
    inside_menu.add_radiobutton(label=i, variable=item_var, command=lambda i=i: gastos_meses(i))
menu["menu"] = inside_menu
# Auxiliares
auxiliar = tb.Label(text="")
separador = tb.Separator(bootstyle="primary")

# Mainloop
if __name__ == "__main__":
    root.mainloop()