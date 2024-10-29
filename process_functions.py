# Función para procesar según el tipo de web (autodoc o regcheck)
from excel_functions import guardar_excel, leer_excel, mapear_resultados, mostrar_mensaje, seleccionar_archivo
from matriculas_functions import buscar_modelos_autodoc, buscar_modelos_carfax

stop_flag = [False]  # Resetear el flag

def iniciar_proceso(tipo, result_text):
    stop_flag[0] = False  # Resetear el flag

    # Seleccionar archivo
    filepath = seleccionar_archivo()
    if not filepath:
        mostrar_mensaje(result_text, "No se seleccionó ningún archivo.")
        return

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

        # Mapear resultados y guardar archivo procesado
        mapear_resultados(df, resultados)
        save_filepath = guardar_excel(df, filepath)
        
        # Mostrar mensaje de éxito
        mostrar_mensaje(result_text, f"Archivo procesado correctamente en {save_filepath}")
    except Exception as e:
        mostrar_mensaje(result_text, f"Hubo un problema al procesar el archivo: {e}")