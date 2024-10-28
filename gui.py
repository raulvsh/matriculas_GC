import tkinter as tk
from tkinter import filedialog, messagebox
import main  # Importar las funciones desde main.py
import os

# Función para mostrar el modelo del coche a partir de la matrícula ingresada
def mostrar_modelo():
    matricula = entry_matricula.get()
    if matricula:
        modelo = main.buscar_modelo_matricula(matricula)  # Asegúrate de que esto esté bien vinculado
        result_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto
        result_text.insert(tk.END, modelo)  # Insertar el resultado
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una matrícula.")

# Función para cargar un archivo Excel, buscar los modelos, y guardar un nuevo archivo
def cargar_archivo_excel():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        try:
            # Procesar el archivo Excel
            df = main.procesar_archivo_excel(filepath)

            # Modificar el nombre del archivo para que incluya "_modelos" antes de la extensión
            filename, file_extension = os.path.splitext(filepath)
            save_filepath = f"{filename}_modelos{file_extension}"

            # Guardar el nuevo archivo Excel con el nuevo nombre
            df.to_excel(save_filepath, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado correctamente en: {save_filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al procesar el archivo: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Buscador de modelos")
root.geometry("650x200")

# Usar un grid para organizar elementos
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Primera columna: Entrada de matrícula, botón de buscar, y botón para cargar Excel
frame_izquierdo = tk.Frame(root)
frame_izquierdo.grid(row=0, column=0, padx=10, pady=10)

# Cuadro de texto para introducir matrícula
label_matricula = tk.Label(frame_izquierdo, text="Matrícula:")
label_matricula.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Cuadro de texto con menor ancho
entry_matricula = tk.Entry(frame_izquierdo, width=20)
entry_matricula.grid(row=1, column=1, pady=5, padx=10)

# Botón para buscar el modelo del coche (ahora alineado a la derecha del cuadro de texto)
btn_buscar = tk.Button(frame_izquierdo, text="Buscar", command=mostrar_modelo)
btn_buscar.grid(row=1, column=2, padx=10, pady=5)  # Colocar en la misma fila (row=1) y en la siguiente columna (column=1)

# Botón para cargar el archivo Excel (alineado a la izquierda)
btn_cargar_excel = tk.Button(frame_izquierdo, text="Cargar archivo Excel", command=cargar_archivo_excel)
btn_cargar_excel.grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky="w")  # Añadido sticky="w" para alinearlo a la izquierda

# Segunda columna: Cuadro de texto para mostrar el modelo
frame_derecho = tk.Frame(root)
frame_derecho.grid(row=0, column=1, padx=0, pady=10, rowspan=4)

#label_modelo = tk.Label(frame_derecho, text="Modelo:")
#label_modelo.grid(row=0, column=0, pady=5, sticky="w")

# Añadir margen horizontal con padx=20 y margen inferior con pady=10
result_text = tk.Text(frame_derecho, width=40, height=10)
result_text.grid(row=1, column=0, pady=10, padx=00)  # Añadido padx para margen lateral y pady(5, 10) para margen inferior

# Ejecutar la interfaz
root.mainloop()
