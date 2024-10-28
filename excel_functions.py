import os
import pandas as pd
from matriculas_functions import buscar_modelo_matricula

# Función para procesar un archivo Excel y buscar los modelos de las matrículas
def cargar_archivo_excel(filepath, result_text):
    try:
        df = pd.read_excel(filepath)

        # Comprobar si tiene una columna de matrículas
        if 'Matrícula' not in df.columns:
            raise ValueError("El archivo no tiene una columna llamada 'Matrícula'.")

        # Crear una nueva columna para los modelos
        df['Modelo'] = df['Matrícula'].apply(lambda matricula: buscar_modelo_matricula(matricula, result_text))

        # Guardar el nuevo archivo Excel con el nuevo nombre
        filename, file_extension = os.path.splitext(filepath)
        save_filepath = f"{filename}_modelos{file_extension}"
        df.to_excel(save_filepath, index=False)
        return df
    except Exception as e:
        raise e
