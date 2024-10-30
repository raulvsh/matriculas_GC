import tkinter as tk
from tkinter import messagebox
from excel_functions import guardar_excel, leer_excel, mapear_resultados, seleccionar_archivo
from matriculas_functions import buscar_modelos_autodoc_es, buscar_modelos_carfax

def iniciar_proceso(tipo, result_text, btn_stop, progress_bar):

    # Seleccionar archivo
    filepath = seleccionar_archivo()
    if not filepath:
        messagebox.showwarning("Advertencia", "No se ha selecionado ningún archivo")  # Mensaje de advertencia
        return
    
    # Muestra el botón `Stop` y la barra de progreso
    btn_stop.config(state='normal')
    btn_stop.grid()

    try:
        # Leer y procesar archivo
        df = leer_excel(filepath)
        matriculas = df['Matrícula'].tolist()

        # Determinar la función de búsqueda según el tipo
        if tipo == "autodoc":
            resultados = buscar_modelos_autodoc_es(matriculas, progress_bar)
        #elif tipo == "regcheck":
        #    resultados = buscar_modelos_regcheck(matriculas)
        #elif tipo == "carfax":
        #    resultados = buscar_modelos_carfax(matriculas, progress_bar)  
        #elif tipo == "prueba":
        #    resultados = asyncio.run(buscar_modelos_prueba(matriculas))
        else:
            raise ValueError("Tipo de procesamiento desconocido.\n")
        
        btn_stop.grid_remove()
        progress_bar.stop() 

        # Mapear resultados y guardar archivo procesado
        mapear_resultados(df, resultados)
        save_filepath = guardar_excel(df, filepath)

        # Mostrar mensaje de éxito
        result_text.insert(tk.END, f"Archivo guardado correctamente en:\n {save_filepath}\n")

    except Exception as e:
        print("Exception", e)
