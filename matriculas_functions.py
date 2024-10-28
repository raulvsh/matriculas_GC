import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
import requests


def iniciar_driver():
    return webdriver.Chrome()  # O el driver que estés utilizando

def permitir_cookies(driver):
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    allow_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Permitir todas las cookies')]"))
    )
    allow_cookies_button.click()  # Haz clic en el botón

def buscar_modelos_autodoc(matriculas):
    resultados = {}
    for matricula in matriculas:
        driver = None
        try:

            driver = iniciar_driver()

            # Abre la página correspondiente
            driver.get("https://www.autodoc.es/")
            #driver.get("https://www.carfax.eu/es")


            #permitir_cookies(driver)
            
            

            # Espera hasta que el campo de búsqueda esté presente (Autodoc)
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "kba1"))
            )

            # Espera hasta que el campo de búsqueda esté presente (Carfax)
            #search_box = WebDriverWait(driver, 10).until(
            #    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Introduce matrícula o bastidor']"))
            #)

            search_box.clear() 
            search_box.send_keys(matricula)
            search_box.send_keys(Keys.RETURN)

            # Temporizador para esperar hasta que el título cambie
            start_time = time.time()
            original_title = "AUTODOC España - tienda online de recambios coche con más de 4 millones de repuestos coches"
            #original_title = "Comprueba la matrícula y obtén el historial del coche | CARFAX"

            title_changed = False


            while time.time() - start_time < 6:  # Espera hasta 6 segundos
                current_title = driver.title
                if current_title != original_title:
                    title_changed = True
                    break
                time.sleep(1)  # Espera medio segundo antes de volver a verificar

            # Extrae el modelo del vehículo si el título ha cambiado
            if title_changed:
                modelo = current_title.split(" | ")[0]
                modelo = modelo.replace("Recambios ", "").strip()
                resultados[matricula] = modelo  # Almacena el resultado





            else:
                print(f"No se encontró modelo para la matrícula: {matricula} en 6 segundos.")


        except Exception as e:
            resultados[matricula] = f"Error: {str(e)}"
            messagebox.showerror("Error", f"Error al abrir la página: {e}")

        finally:
            if driver:
                driver.quit()

    return resultados  # Devuelve los resultados de las búsquedas


def buscar_modelos_regcheck(matriculas):
        resultados = {}
        username = "raulvsh@gmail.com"
        for matricula in matriculas:
            url = f"http://www.regcheck.org.uk/api/reg.asmx/CheckSpain?RegistrationNumber={matricula}&username={username}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    resultados[matricula] = response.json().get("Model", "Modelo no encontrado")
                else:
                    resultados[matricula] = "Error en API"
            except Exception as e:
                resultados[matricula] = f"Error: {e}"
        return resultados