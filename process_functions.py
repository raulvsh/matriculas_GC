# Función para procesar según el tipo de web (autodoc o regcheck)
import tkinter as tk
from excel_functions import guardar_excel, leer_excel, mapear_resultados, seleccionar_archivo
from matriculas_functions import buscar_modelos_autodoc, buscar_modelos_carfax

#stop_flag = [False]  # Resetear el flag

def iniciar_proceso(tipo, result_text, btn_stop):

    # Seleccionar archivo
    filepath = seleccionar_archivo()
    if not filepath:
        result_text.insert(tk.END, "No se seleccionó ningún archivo.")
        return
    
    # Muestra el botón `Stop`
    btn_stop.grid()

    try:
        # Leer y procesar archivo
        df = leer_excel(filepath)
        matriculas = df['Matrícula'].tolist()

        # Determinar la función de búsqueda según el tipo
        if tipo == "autodoc":
            resultados = buscar_modelos_autodoc(matriculas)
        #elif tipo == "regcheck":
        #    resultados = buscar_modelos_regcheck(matriculas)
        elif tipo == "carfax":
            resultados = buscar_modelos_carfax(matriculas)  
        else:
            raise ValueError("Tipo de procesamiento desconocido.")
        
        btn_stop.grid_remove()

        # Mapear resultados y guardar archivo procesado
        mapear_resultados(df, resultados)
        save_filepath = guardar_excel(df, filepath)

        
        # Mostrar mensaje de éxito
        result_text.insert(tk.END, f"Archivo procesado correctamente en {save_filepath}")

        #mostrar_mensaje(result_text, f"Archivo procesado correctamente en {save_filepath}")
    except Exception as e:
        #result_text.insert(tk.END, f"Hubo un problema al procesar el archivo: {e}")
        print("Exception", e)
