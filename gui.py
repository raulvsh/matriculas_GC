import tkinter as tk
from tkinter import filedialog, messagebox
from excel_functions import seleccionar_archivo
import threading
from matriculas_functions import busqueda_individual, stop_flag
from process_functions import iniciar_proceso, stop_flag

# Función para crear la interfaz gráfica
def crear_interfaz():
    global entry_matricula, result_text, btn_buscar, btn_stop

    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Buscador de modelos")
    root.geometry("730x280")
    root.iconbitmap("./assets/logo.ico")

    # Segunda columna: Cuadro de texto para mostrar el modelo
    frame_derecho = tk.Frame(root)
    frame_derecho.grid(row=0, column=1, padx=0, pady=10, rowspan=4)

    result_text = tk.Text(frame_derecho, width=50, height=15)
    result_text.grid(row=1, column=0, pady=10, padx=00)

    # Crear estilo en negrita
    result_text.tag_config("bold", font=("Helvetica", 12, "bold"))
    # Mostrar el mensaje en negrita
    result_text.insert("end", "Buscador de modelos por matrícula\n", "bold")

    # Primera columna: Entrada de matrícula, botones para cargar Excel
    frame_izquierdo = tk.Frame(root)
    frame_izquierdo.grid(row=0, column=0, padx=10, pady=10)

    # Cuadro de texto para introducir matrícula
    label_matricula = tk.Label(frame_izquierdo, text="Matrícula:")
    label_matricula.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    # Cuadro de texto con menor ancho
    entry_matricula = tk.Entry(frame_izquierdo, width=20)
    entry_matricula.grid(row=1, column=1, pady=5, padx=10)

# Función que maneja la búsqueda individual y simula el efecto visual del botón presionado
    def on_enter_key(event, entry, result_text):
        btn_buscar.config(relief=tk.SUNKEN)  # Cambia el relieve para simular el botón presionado
        btn_buscar.update_idletasks()  # Actualiza la interfaz para que el cambio se vea de inmediato
        busqueda_individual(entry, result_text)  # Llama a la función de búsqueda
        # Usa after para restaurar el botón tras 100ms
        root.after(100, lambda: btn_buscar.config(relief=tk.RAISED))

    # Botón para buscar el modelo del coche
    btn_buscar = tk.Button(frame_izquierdo, text="Buscar", command=lambda: busqueda_individual(entry_matricula, result_text))
    btn_buscar.grid(row=1, column=2, padx=10, pady=5)
    entry_matricula.bind("<Return>", lambda event: on_enter_key(event, entry_matricula, result_text))




    # Grupo de botones para Autodoc
    label_autodoc = tk.Label(frame_izquierdo, text="Autodoc:")
    label_autodoc.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_autodoc = tk.Button(
        frame_izquierdo,
        text="Cargar archivo",
        command=lambda: iniciar_proceso("autodoc", result_text)
    )
    btn_cargar_autodoc.grid(row=2, column=1, pady=10, padx=10, columnspan=2, sticky="w")

    # Grupo de botones para RegCheck (en caso de que se comprase una suscripción)
    '''label_regcheck = tk.Label(frame_izquierdo, text="RegCheck:")
    label_regcheck.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_regcheck = tk.Button(frame_izquierdo, text="Cargar archivo", command=lambda: procesar("regcheck", result_text))
    btn_cargar_regcheck.grid(row=3, column=1, pady=10, padx=10, columnspan=2, sticky="w")'''

    # Grupo de botones para Carfax
    label_carfax = tk.Label(frame_izquierdo, text="Carfax:")
    label_carfax.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_carfax = tk.Button(
        frame_izquierdo,
        text="Cargar archivo",
        command=lambda: iniciar_proceso("carfax", result_text, btn_stop)
    )
    btn_cargar_carfax.grid(row=4, column=1, pady=10, padx=10, columnspan=2, sticky="w")


    btn_stop = tk.Button(
        frame_izquierdo,
        text="Stop",
        bg="red",
        fg="white",
        command=lambda: toggle_stop(),
        width=8,    # Ajusta el ancho del botón
        height=2,    # Ajusta la altura del botón
        font=("Arial", 10, "bold")  # Cambia el tamaño y estilo de la fuente
    )
    btn_stop.grid(row=5, column=1, padx=10, pady=5)
    btn_stop.grid_remove()  # Ocultar el botón inicialmente

    def toggle_stop():
        stop_flag[0] = True
        btn_stop.grid_remove()  # Ocultar el botón después de pulsarlo


    # Ejecutar la interfaz
    root.mainloop()
