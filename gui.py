import tkinter as tk
from tkinter import ttk, messagebox  # Importar solo lo necesario
from matriculas_functions import busqueda_individual_autodoc
from process_functions import iniciar_proceso
import threading
from global_vars import stop_flag 
import os
import sys

def get_absolute_path(relative_path):
    try:
        # PyInstaller crea una carpeta temporal y almacena el ejecutable allí
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Función para crear la interfaz gráfica
def crear_interfaz():
    global entry_matricula, result_text, btn_buscar, btn_stop

    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Buscador de modelos")
    root.geometry("740x280")
    icon_path = get_absolute_path("assets/logo2.ico")
    root.wm_iconbitmap(icon_path)
    #root.wm_iconbitmap("./assets/logo.ico")

    # Segunda columna: Cuadro de texto para mostrar el modelo
    frame_derecho = tk.Frame(root)
    frame_derecho.grid(row=0, column=1, padx=(10,00), pady=10, rowspan=4)

    result_text = tk.Text(frame_derecho, width=50, height=15)
    result_text.grid(row=1, column=0, pady=10, padx=(10,0))

    # Crear estilo en negrita
    result_text.tag_config("bold", font=("Helvetica", 12, "bold"))
    # Mostrar el mensaje en negrita
    result_text.insert("end", "Buscador de modelos por matrícula\n", "bold")

    # Primera columna: Entrada de matrícula, botones para cargar Excel
    frame_izquierdo = tk.Frame(root)
    frame_izquierdo.grid(row=0, column=0, padx=(10,0), pady=10)

    # Cuadro de texto para introducir matrícula
    label_matricula = tk.Label(frame_izquierdo, text="Matrícula:")
    label_matricula.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Cuadro de texto con menor ancho
    entry_matricula = tk.Entry(frame_izquierdo, width=20)
    entry_matricula.grid(row=1, column=1, pady=10, padx=10)

    # Botón para buscar el modelo del coche
    btn_buscar = tk.Button(frame_izquierdo, text="Buscar", command=lambda: validar_matricula())
    btn_buscar.grid(row=1, column=2, padx=10, pady=10)

    # Asignar la función al presionar "Intro"
    entry_matricula.bind("<Return>", lambda event: on_enter_key(event, entry_matricula, result_text, progress_bar))


    # Grupo de botones para Autodoc
    label_autodoc = tk.Label(frame_izquierdo, text="Autodoc:")
    label_autodoc.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_autodoc = tk.Button(
        frame_izquierdo,
        text="Cargar archivo",
        command=lambda: threading.Thread(target=iniciar_proceso, args=("autodoc", result_text, btn_stop, progress_bar)).start()
    )
    btn_cargar_autodoc.grid(row=2, column=1, pady=10, padx=10, columnspan=2, sticky="w")

    # Grupo de botones para RegCheck (en caso de que se comprase una suscripción)
    '''label_regcheck = tk.Label(frame_izquierdo, text="RegCheck:")
    label_regcheck.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_regcheck = tk.Button(frame_izquierdo, text="Cargar archivo", command=lambda: procesar("regcheck", result_text))
    btn_cargar_regcheck.grid(row=3, column=1, pady=10, padx=10, columnspan=2, sticky="w")'''

    # Grupo de botones para Carfax
    '''label_carfax = tk.Label(frame_izquierdo, text="Carfax:")
    label_carfax.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    btn_cargar_carfax = tk.Button(
        frame_izquierdo,
        text="Cargar archivo",
        command=lambda: threading.Thread(target=iniciar_proceso, args=("carfax", result_text, btn_stop)).start()
    )
    btn_cargar_carfax.grid(row=4, column=1, pady=10, padx=10, columnspan=2, sticky="w")'''

    # Botón de prueba para iniciar proceso con argumento "prueba"
    '''btn_prueba = tk.Button(
        frame_izquierdo,
        text="Prueba",
        command=lambda: threading.Thread(target=iniciar_proceso, args=("prueba", result_text, btn_stop)).start()
    )'''
    #btn_prueba.grid(row=5, column=1, pady=10, padx=10, columnspan=2, sticky="w")

    # Placeholder vacío que ocupará el mismo espacio que el botón STOP
    placeholder = tk.Label(frame_izquierdo, font=("Arial", 10, "bold"), width=8, height=2,)  # Crea un Label vacío con el mismo tamaño
    placeholder.grid(row=6, column=1, padx=10, pady=46)  # Coloca el placeholder en la misma posición que el botón STOP

    # Botón de STOP
    btn_stop = tk.Button(
        frame_izquierdo,
        text="STOP",
        bg="red",
        fg="white",
        command=lambda: toggle_stop(),
        width=8,
        height=2,
        font=("Arial", 10, "bold")
    )
    btn_stop.grid(row=6, column=1, padx=10, pady=43)
    btn_stop.grid_remove()

    # Crear la barra de progreso
    progress_bar = ttk.Progressbar(frame_izquierdo)
    progress_bar.grid(row=11, column=0, columnspan=3, padx=10, pady=(10, 10), sticky='ew')  # Extender a ambas columnas y alinear en la parte inferior


    def toggle_stop():
        stop_flag[0] = True
        btn_stop.grid_remove()  # Ocultar el botón después de pulsarlo
        progress_bar.stop()  # Detener la barra de progreso
        result_text.insert(tk.END, f"Proceso detenido\n")

    def on_enter_key(event, entry, result_text, progress_bar):
        btn_buscar.config(relief=tk.SUNKEN)  # Cambia el relieve para simular el botón presionado
        btn_buscar.update_idletasks()  # Actualiza la interfaz para que el cambio se vea de inmediato

        # Ejecuta la búsqueda en un hilo separado para evitar bloqueo
        validar_matricula()

        # Usa after para restaurar el botón tras 100ms
        root.after(100, lambda: btn_buscar.config(relief=tk.RAISED))

    # Botón para buscar el modelo del coche
    def validar_matricula():
        matricula = entry_matricula.get().strip()  # Obtener el texto y eliminar espacios en blanco
        if not matricula:  # Verificar si está vacío
            messagebox.showwarning("Advertencia", "Introduce una matrícula")  # Mensaje de advertencia
        else:
            threading.Thread(target=busqueda_individual_autodoc, args=(entry_matricula, result_text, progress_bar)).start()

    # Ejecutar la interfaz
    root.mainloop()
