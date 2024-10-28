import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox

def iniciar_driver():
    return webdriver.Chrome()  # O el driver que estés utilizando

def permitir_cookies(driver):
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    allow_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Permitir todas las cookies')]"))
    )
    allow_cookies_button.click()  # Haz clic en el botón

def buscar_modelos_matriculas(matriculas):
    resultados = {}
    try:
        for matricula in matriculas:
            driver = iniciar_driver()

            # Abre la página de Autodoc
            driver.get("https://www.autodoc.es/")
            permitir_cookies(driver)
        
            # Espera hasta que el campo de búsqueda esté presente
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "kba1"))
            )

            search_box.clear() 
            search_box.send_keys(matricula)
            search_box.send_keys(Keys.RETURN)

            # Temporizador para esperar hasta que el título cambie
            start_time = time.time()
            original_title = "AUTODOC España - tienda online de recambios coche con más de 4 millones de repuestos coches"
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

            driver.quit()  # Cierra el navegador

    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir la página: {e}")

    return resultados  # Devuelve los resultados de las búsquedas