import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from global_vars import stop_flag


def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Activar modo headless
    chrome_options.add_argument("--no-sandbox")  # Para evitar problemas en entornos restringidos
    chrome_options.add_argument("--disable-dev-shm-usage")  # Para evitar errores de memoria
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    return webdriver.Chrome(options=chrome_options)  # O el driver que estés utilizando

def permitir_cookies(driver):
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    allow_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Permitir todas las cookies')]"))
    )
    allow_cookies_button.click()  # Haz clic en el botón

def buscar_modelos_autodoc_es(matriculas, progress_bar):
    resultados = {}
    stop_flag[0]=False

    config_progress_bar(matriculas, progress_bar)

    for i, matricula in enumerate(matriculas):
        if stop_flag[0]:  # Verificar si se debe detener
            if driver:
                driver.quit()
            break
        driver = None
        try:
            update_progress_bar(progress_bar, i + 1, len(matriculas))

            driver = iniciar_driver()
            driver.get("https://www.autodoc.es/")
            #permitir_cookies(driver)   #Tarda más si se permiten las cookies, no es necesario          

            # Espera hasta que el campo de búsqueda esté presente (Autodoc)
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
                if stop_flag[0]:  # Verificar si se debe detener durante la espera
                    break
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

        finally:
            if driver:
                driver.quit()

    return resultados 

def config_progress_bar(matriculas, progress_bar):
    if len(matriculas) == 1:
        progress_bar.config(mode='indeterminate')
        progress_bar.start(10)  # Iniciar la barra de progreso indefinida
    else:
        progress_bar.config(mode='determinate'),

def update_progress_bar(progress_bar, current, total):
    progress_percentage = (current / total) * 100
    progress_bar['value'] = progress_percentage-5
    progress_bar.update_idletasks()

'''def buscar_modelos_carfax(matriculas, progress_bar):
    resultados = {}
    stop_flag[0] = False

    for matricula in matriculas:
        if stop_flag[0]:  # Verificar si se debe detener
            if driver:
                driver.quit()
            break
        
        driver = None
        try:
            driver = iniciar_driver()  # Reutilizar función de inicialización del driver
            driver.get("https://www.carfax.eu/es")
            
            # Espera hasta que el campo de búsqueda esté presente
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Introduce matrícula o bastidor']"))
            )

            search_box.clear()
            search_box.send_keys(matricula)
            search_box.send_keys(Keys.RETURN)

            # Temporizador para esperar hasta que el título cambie
            start_time = time.time()
            original_title = "Comprueba la matrícula y obtén el historial del coche | CARFAX"
            title_changed = False

            while time.time() - start_time < 6:  # Espera hasta 6 segundos
                if stop_flag[0]:  # Verificar si se debe detener durante la espera
                    break
                current_title = driver.title
                if current_title != original_title:
                    title_changed = True
                    break
                time.sleep(0.5)

            # Extrae el modelo del vehículo si el título ha cambiado
            if title_changed:
                try:
                    # Espera y obtiene el texto de marca y modelo
                    marca_modelo_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Marca y modelo')]"))
                    )
                    marca_modelo = marca_modelo_element.text.split(":")[1].strip()  # Extrae el modelo
                    resultados[matricula] = marca_modelo
                except Exception:
                    resultados[matricula] = "Modelo no encontrado"
            else:
                print(f"No se encontró modelo para la matrícula: {matricula} en 6 segundos.")
                resultados[matricula] = "Timeout al buscar modelo"
        
        except Exception as e:
            resultados[matricula] = f"Error: {str(e)}"

        finally:
            if driver:
                driver.quit()
    
    return resultados  # Devuelve los resultados de las búsquedas
    '''

def busqueda_individual_autodoc(entry_matricula, result_text, progress_bar):
    matricula = entry_matricula.get()
    progress_bar.config(mode='indeterminate')
    progress_bar.start(10)  # Iniciar la barra de progreso indefinida
    resultado = buscar_modelos_autodoc_es([matricula], progress_bar)

    if matricula in resultado:
        result_text.insert(tk.END, f"Matrícula: {matricula}\n")
        result_text.insert(tk.END, f"Modelo: {resultado[matricula]}\n\n")
    else:
        result_text.insert(tk.END, "No se encontró el modelo para esta matrícula.")
    progress_bar.stop()
    progress_bar.config(mode='determinate')



'''async def buscar_modelos_prueba(matriculas):
    print(matriculas)
    resultados = {}
    stop_flag[0] = False  # Resetear el flag al inicio

    # Inicializa el navegador asincrónicamente
    browser = await uc.start(headless=False)  # Configuración del navegador

    for matricula in matriculas:
        if stop_flag[0]:  # Verificar si se debe detener
            break
        
        try:
            # Navega a la página principal de Carfax
            await browser.get("https://www.autodoc.es/")
            
            # Espera hasta que el campo de búsqueda esté presente (Autodoc)
            search_box = WebDriverWait(browser, 10).until(
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
                if stop_flag[0]:  # Verificar si se debe detener durante la espera
                    break
                current_title = browser.title()
                if current_title != original_title:
                    title_changed = True
                    break
                asyncio.sleep(1)  # Espera un segundo antes de volver a verificar

            # Extrae el modelo del vehículo si el título ha cambiado
            if title_changed:
                modelo = (await browser.title()).split(" | ")[0]
                modelo = modelo.replace("Recambios ", "").strip()
                resultados[matricula] = modelo  # Almacena el resultado
            else:
                print(f"No se encontró modelo para la matrícula: {matricula} en 6 segundos.")
                resultados[matricula] = "Timeout al buscar modelo"

        except Exception as e:
            resultados[matricula] = f"Error: {str(e)}"

    await browser.close()
    return resultados  # Devuelve los resultados de las búsquedas
    '''