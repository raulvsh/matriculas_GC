import os
import pandas as pd
from matriculas_functions import buscar_modelos_matriculas  # Cambiar la función importada

# Función para procesar un archivo Excel y buscar los modelos de las matrículas
def procesar_archivo_excel(filepath, result_text):
    try:
        df = pd.read_excel(filepath)

        # Comprobar si tiene una columna de matrículas
        if 'Matrícula' not in df.columns:
            raise ValueError("El archivo no tiene una columna llamada 'Matrícula'.")

        # Obtener la lista de matrículas
        matriculas = df['Matrícula'].tolist()
        print("Matriculas: ", matriculas)

        # Llamar a la función que busca todos los modelos de matrícula
        resultados = buscar_modelos_matriculas(matriculas)  # Llama a la función optimizada
        print("Modelos: ", resultados)

        # Crear una nueva columna para los modelos usando los resultados
        df['Modelo'] = df['Matrícula'].map(resultados)

        # Guardar el nuevo archivo Excel con el nuevo nombre
        filename, file_extension = os.path.splitext(filepath)
        save_filepath = f"{filename}_modelos{file_extension}"
        df.to_excel(save_filepath, index=False)
        print("df ",df)
        return df
    except Exception as e:
        raise e
