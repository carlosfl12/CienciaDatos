import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import importlib
import meteoritedf
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

csv_path = ""

def open_csv():
    global csv_path
    file = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    if file:
        lbl_path.config(text=f"Archivo seleccionado:\n{file}")
        csv_path = file

        # Mostrar el botón de completar cuando haya un archivo
        complete_button.config(state=tk.NORMAL)

        if not csv_path:
            return
        importlib.reload(meteoritedf)
        meteoritedf.load_dataframe(csv_path)

        dataframe = meteoritedf.get_dataframe()
        if dataframe.empty:
            lbl_path.config(text="El DataFrame está vacio")
            return
        
        load_into_combobox(combo, dataframe.columns)
        load_into_combobox(combo2, dataframe.columns)


def complete():
    global csv_path

    if not csv_path:
        return
    
    for widget in graphic.winfo_children():
        widget.destroy()
    
    try:
        fig, ax = plt.subplots()
        num_combo3 = ""
        num_combo4 = ""
        if combobox_function.get() == "Máximo x Columna":
            meteoritedf.create_sum(meteoritedf.get_dataframe(), combo.get(), 5, ax=ax)
            ax.set_ylabel("Cantidad")
        elif combobox_function.get() == "Ubicación mapa":
            if combo3.get().replace(".0", "").isnumeric():
                num_combo3 = int(combo3.get().replace(".0", ""))
            else:
                num_combo3 = combo3.get()

            if combo4.get().replace(".0", "").isnumeric():
                num_combo4 = int(combo4.get().replace(".0", ""))
            else:
                num_combo4 = combo4.get()
            meteoritedf.identify_meteorite(meteoritedf.get_dataframe(), combo.get(), combo2.get(), num_combo4, num_combo3, ax = ax)
        else:
            if combo3.get().replace(".0", "").isnumeric():
                num_combo3 = int(combo3.get().replace(".0", ""))
            else:
                num_combo3 = combo3.get()
            print(num_combo3)
            meteoritedf.build_bar_by_group(meteoritedf.get_dataframe(), combo.get(), combo2.get(), num_combo3, 5, ax=ax)
            ax.set_ylabel("Cantidad")
            ax.set_title(f"{combo3.get()} / {combo2.get()}")

        canvas = FigureCanvasTkAgg(fig, master=graphic)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        lbl_path.config(text=f"Error al cargar el archivo:\n{e}")

def load_into_combobox(combobox : ttk.Combobox, dataframe_columns):
    combobox["state"] = "readonly"
    values = []
    for column in dataframe_columns:
        values.append(column)
    combobox["values"] = values

def get_unique_results(event, combo_event, combobox):
    values = []
    for column in meteoritedf.get_unique_from_column(meteoritedf.get_dataframe(), combo_event.get()):
        values.append(column)
        values.sort()
    combobox["values"] = values    

# Ventana principal
root = tk.Tk()
root.title("Proyecto")

root.geometry("1080x480")
root.minsize(1080, 480)

# Botón para abrir el archivo
open_button = tk.Button(root, text="Abrir CSV", command=open_csv)
open_button.pack(pady=10)

# Etiqueta para mostrar el archivo seleccionado
lbl_path = tk.Label(root, text = "Ningún archivo seleccionado", wraplength=500)
lbl_path.pack(pady=10)

# Cargar en el combobox el nombre de las columnas
combo = ttk.Combobox(state="readonly")
ttk.Label(root, text="Columna 1").pack(padx=10, pady=5)
combo.pack(pady=10)
combo2 = ttk.Combobox(state="readonly")
ttk.Label(root, text="Columna 2").pack(padx=20, pady=5)
combo2.pack(pady = 10)

# Crear un evento para cada vez que se cambie el segundo combobox
# Filtro de combobox
combo3 = ttk.Combobox(state="readonly")
ttk.Label(root, text="Filtrar por").pack(padx=30, pady=10)
combo3.pack(pady=10)

combo4 = ttk.Combobox(state="readonly")
combo4.pack(pady=10)

combo2.bind("<<ComboboxSelected>>", lambda event: get_unique_results(event, combo2, combo3))
combo.bind("<<ComboboxSelected>>", lambda event: get_unique_results(event, combo, combo4))

# Seleccionar la función que se quiere realizar
combobox_function = ttk.Combobox(state="readonly", values=("Máximo x Columna", "Columnas y Condición", "Ubicación mapa"))
combobox_function.pack(pady=15)

# Botón de completar
complete_button = tk.Button(root, text="Completar", state=tk.DISABLED, command=complete)
complete_button.pack(pady=10)

# Frame para el gráfico
graphic = tk.Frame(root)
graphic.pack(expand=True, fill="both")

root.mainloop()


# def search():
#     print(get_group(df, column1.get().title(), column2.get().title(), group_by.get().title(), 5))