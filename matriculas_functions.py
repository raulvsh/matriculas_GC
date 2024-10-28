import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox

def buscar_modelos_matriculas(matriculas):
    driver = webdriver.Chrome()  # Asegúrate de que ChromeDriver esté en el PATH
    resultados = {}

    try:
        # Abre la página de Autodoc
        driver.get("https://www.autodoc.es/")
        
        # Espera hasta que el campo de búsqueda esté presente
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kba1"))
        )

        for matricula in matriculas:
            try:
                search_box.clear()  # Limpia el campo de búsqueda
                search_box.send_keys(matricula)
                search_box.send_keys(Keys.RETURN)

                # Espera hasta que el título de la página cambie
                '''WebDriverWait(driver, 10).until(
                    lambda d: d.title != "Autodoc"
                )'''

                time.sleep(5)

                # Extrae el modelo del vehículo
                modelo = driver.title
                if modelo:
                    modelo = modelo.split(" | ")[0]
                    modelo = modelo.replace("Recambios ", "").strip()

                resultados[matricula] = modelo  # Almacena el resultado

            except Exception as e:
                resultados[matricula] = f"Error: {e}"  # Almacena el error

    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir la página: {e}")
    finally:
        driver.quit()  # Cierra el navegador

    return resultados  # Devuelve los resultados de las búsquedas

'''


# Función para obtener el modelo del vehículo a partir de la matrícula usando Selenium
def buscar_modelo_matricula(matricula, result_text):
    driver = webdriver.Chrome()  # Asegúrate de que ChromeDriver esté en el PATH
    modelo = "No encontrado"

    try:
        # Abre la página de Autodoc
        driver.get("https://www.autodoc.es/")

        # Espera hasta que el campo de búsqueda esté presente
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kba1"))
        )

        search_box.clear()
        search_box.send_keys(matricula)
        search_box.send_keys(Keys.RETURN)

        # Espera hasta que el título de la página cambie
        WebDriverWait(driver, 10).until(
            lambda d: d.title != "Autodoc"
        )

        # Extrae el modelo del vehículo
        modelo = driver.title
        if modelo:
            modelo = modelo.split(" | ")[0]
            modelo = modelo.replace("Recambios ", "").strip()

        

        #mostrar_mensaje(result_text, modelo)  # Mostrar el resultado en el cuadro de texto

    except Exception as e:
        print("Excepcion")
        #mostrar_mensaje(result_text, f"Error al buscar la matrícula {matricula}: {e}")
    finally:
        driver.quit()  # Cierra el navegador

    return modelo



'''