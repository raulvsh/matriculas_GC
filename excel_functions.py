import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Funciones comunes
def mostrar_mensaje(text_widget, mensaje):
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, mensaje)

# Función para seleccionar el archivo y devolver la ruta
def seleccionar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return filepath

def leer_excel(filepath):
    df = pd.read_excel(filepath)
    if 'Matrícula' not in df.columns:
        raise ValueError("El archivo no tiene una columna llamada 'Matrícula'.")
    return df

def mapear_resultados(df, resultados):
    df['Modelo'] = df['Matrícula'].map(resultados)

# Función para guardar el archivo Excel con el sufijo 'modelos'
def guardar_excel(df, filepath):
    filename, file_extension = os.path.splitext(filepath)
    save_filepath = f"{filename}_modelos{file_extension}"
    df.to_excel(save_filepath, index=False)
    return save_filepath

# Función para procesar autodoc
'''def procesar_autodoc(filepath):
    df = leer_excel(filepath)
    matriculas = df['Matrícula'].tolist()
    resultados = buscar_modelos_autodoc(matriculas)  # Usando la función optimizada existente
    mapear_resultados(df, resultados)
    return guardar_excel(df, filepath, "modelos_autodoc")'''

# Función para procesar RegCheck
'''def procesar_regcheck(filepath):    
    df = leer_excel(filepath)
    matriculas = df['Matrícula'].tolist()
    resultados = buscar_modelos_regcheck(matriculas)
    mapear_resultados(df, resultados)
    return guardar_excel(df, filepath, "modelos_regcheck")'''