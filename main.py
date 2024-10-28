import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para obtener el modelo del vehículo a partir de la matrícula usando Selenium
def buscar_modelo_matricula(matricula):
    driver = webdriver.Chrome()  # Asegúrate de que ChromeDriver esté en el PATH
    modelo = "No encontrado"

    try:
        # Abre la página de Autodoc
        driver.get("https://www.autodoc.es/")
        #time.sleep(2)  # Espera a que la página cargue

        # Espera hasta que el campo de búsqueda esté presente
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kba1"))
        )

        # Encuentra el campo de búsqueda de matrícula
        #search_box = driver.find_element(By.ID, "kba1")  # Selector del campo de matrícula
        search_box.clear()
        search_box.send_keys(matricula)
        search_box.send_keys(Keys.RETURN)

        # Espera para que la página muestre los resultados
        #time.sleep(5)

                # Espera hasta que el título de la página cambie (lo que indica que la búsqueda se ha realizado)
        WebDriverWait(driver, 10).until(
            lambda d: d.title != "Autodoc"  # Espera hasta que el título no sea "Autodoc"
        )

        # Extrae el modelo del vehículo
        #modelo = driver.find_element(By.CSS_SELECTOR, "#output strong").text
        modelo = driver.title
         # Si necesitas solo el modelo, puedes procesar el título para extraer la parte relevante
        if modelo:
            # Ejemplo: "Recambios Audi A4 B6 1.9 TDI 130 cv Gasóleo 2000 - 2004 AVF, AWX | A4 8E2 catálogo de repuestos AUTODOC"
            # Extraer solo la parte relevante del modelo
            modelo = modelo.split(" | ")[0]  # Mantiene solo la parte antes del símbolo "|"
            modelo = modelo.replace("Recambios ", "").strip()  # Elimina la palabra "Recambios" y recorta espacios
    except Exception as e:
        print(f"Error al buscar la matrícula {matricula}: {e}")
    finally:
        driver.quit()  # Cierra el navegador

    return modelo

# Función para procesar un archivo Excel y buscar los modelos de las matrículas
def procesar_archivo_excel(filepath):
    try:
        df = pd.read_excel(filepath)

        # Comprobar si tiene una columna de matrículas
        if 'Matrícula' not in df.columns:
            raise ValueError("El archivo no tiene una columna llamada 'Matrícula'.")

        # Crear una nueva columna para los modelos
        df['Modelo'] = df['Matrícula'].apply(buscar_modelo_matricula)

        return df
    except Exception as e:
        raise e
