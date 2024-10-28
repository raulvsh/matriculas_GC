import tkinter as tk
from tkinter import filedialog, messagebox
from excel_functions import procesar, seleccionar_archivo
import threading




    
'''# Función para mostrar el modelo del coche a partir de la matrícula ingresada
def mostrar_modelo(entry_matricula, result_text):
    matricula = entry_matricula.get()
    if matricula:
        modelo = buscar_modelos_autodoc([matricula]) 
        
        if modelo:
            mostrar_mensaje(result_text, modelo[matricula])
        else:
            mostrar_mensaje(result_text, "No se encontró el modelo.")
    else:
        mostrar_mensaje(result_text, "Por favor, ingresa una matrícula.")'''

# Función para manejar la búsqueda en un hilo
def iniciar_busqueda(entry_matricula, result_text):
    # Deshabilitar el botón de búsqueda y habilitar el botón de stop
    btn_buscar.config(state=tk.DISABLED)
    btn_stop.config(state=tk.NORMAL)

    # Ejecutar búsqueda
    #mostrar_modelo(entry_matricula, result_text)

    # Volver a habilitar el botón de búsqueda
    btn_buscar.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)

# Función para cargar un archivo Excel
'''
def cargar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        try:
            df = procesar_archivo_excel(filepath, result_text)
            mostrar_mensaje(result_text, f"Archivo guardado correctamente en {filepath} \n {len(df)} matrículas procesadas.")
        except Exception as e:
            mostrar_mensaje(result_text, f"Hubo un problema al procesar el archivo: {e}")
'''

# Función para crear la interfaz gráfica
def crear_interfaz():
    global entry_matricula, result_text, btn_buscar, btn_stop

    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Buscador de modelos")
    root.geometry("720x250")
    # Segunda columna: Cuadro de texto para mostrar el modelo
    frame_derecho = tk.Frame(root)
    frame_derecho.grid(row=0, column=1, padx=0, pady=10, rowspan=4)

    result_text = tk.Text(frame_derecho, width=50, height=15)
    result_text.grid(row=1, column=0, pady=10, padx=00)


    # Primera columna: Entrada de matrícula, botón de buscar, y botón para cargar Excel
    frame_izquierdo = tk.Frame(root)
    frame_izquierdo.grid(row=0, column=0, padx=10, pady=10)

    # Cuadro de texto para introducir matrícula
    label_matricula = tk.Label(frame_izquierdo, text="Matrícula:")
    label_matricula.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    # Cuadro de texto con menor ancho
    entry_matricula = tk.Entry(frame_izquierdo, width=20)
    entry_matricula.grid(row=1, column=1, pady=5, padx=10)

    # Botón para buscar el modelo del coche
    btn_buscar = tk.Button(frame_izquierdo, text="Buscar", command=lambda: threading.Thread(target=iniciar_busqueda, args=(entry_matricula, result_text)).start())
    btn_buscar.grid(row=1, column=2, padx=10, pady=5)

    btn_cargar_autodoc = tk.Button(frame_izquierdo, text="Procesar autodoc", command=lambda:procesar("autodoc", result_text))
    btn_cargar_autodoc.grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky="w")

    btn_cargar_regcheck = tk.Button(frame_izquierdo, text="Procesar RegCheck", command=lambda: procesar("regcheck", result_text))
    btn_cargar_regcheck.grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky="w")

    btn_stop = tk.Button(frame_izquierdo, text="Stop", bg="red", command=None)
    btn_stop.grid(row=2, column=2, padx=10, pady=5)



    # Ejecutar la interfaz
    root.mainloop()
