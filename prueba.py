import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configuración inicial
matriculas = ["8909BJW", "0672CNB", "8909BJW"]  # Lista de matrículas
resultados = []

# Inicialización del navegador con Selenium
driver = webdriver.Chrome()  # Asegúrate de que ChromeDriver esté en el PATH

try:
    for matricula in matriculas:
        # Abre la página de CARFAX España
        #driver.get("https://www.carfax.eu/es")
        driver.get("https://www.seisenlinea.com/calcular-fecha-matriculacion/")

        # Encuentra el campo de búsqueda de matrícula
        time.sleep(2)  # Espera por si hay elementos que cargan con retardo
        #search_box = driver.find_element(By.NAME, "vin-search-defaultWithoutContainer")  # Actualiza si el selector es distinto
        search_box = driver.find_element(By.NAME, "matricula")  # Actualiza si el selector es distinto


        # Introduce la matrícula en el campo y envía
        search_box.clear()
        search_box.send_keys(matricula)
        search_box.send_keys(Keys.RETURN)

        # Espera para que la página muestre los resultados
        time.sleep(5)

        # Extrae el modelo del vehículo
        try:
            # Cambia el selector según la estructura de la página
            #modelo = driver.find_element(By.CLASS_NAME, "makeAndModelLabel").text  
            modelo = driver.find_element(By.CSS_SELECTOR, "#output strong").text

            #const texto = document.querySelector('#output strong').textContent;

            resultados.append({"Matricula": matricula, "Modelo": modelo})
        except Exception as e:
            print(f"Error al extraer datos para {matricula}: {e}")
            resultados.append({"Matricula": matricula, "Modelo": "No encontrado"})

        # Pausa para evitar bloqueos por tráfico
        time.sleep(3)
finally:
    driver.quit()  # Cierra el navegador

# Guarda los resultados en un archivo CSV
print(resultados)
df = pd.DataFrame(resultados)
df.to_csv("resultados_carfax.csv", index=False)
print("Consulta completada y guardada en 'resultados_carfax.csv'")
