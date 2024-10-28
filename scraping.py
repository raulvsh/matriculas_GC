import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Inicializar el WebDriver
def init_driver():
    # Usa el WebDriver Manager para obtener la última versión de ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

# Función para buscar el modelo de coche dado un número de matrícula
def buscar_modelo_matricula(matricula):
    driver = init_driver()
    
    try:
        # Navegar a la página web
        driver.get("https://www.oscaro.es")  # Cambia esta URL a la correcta

        # Esperar que la página cargue (puedes ajustar el tiempo o usar WebDriverWait)
        time.sleep(2)

        # Encontrar el campo de matrícula e introducir la matrícula
        campo_matricula = driver.find_element(By.ID, "vehicle-input-plate")  # Cambia el ID si es necesario
        campo_matricula.clear()
        campo_matricula.send_keys(matricula)

        # Hacer clic en el botón "Ok" (asegúrate de que el selector es correcto)
        boton_buscar = driver.find_element(By.CSS_SELECTOR, ".btn-secondary.btn-submit")  # Cambia el selector si es necesario
        boton_buscar.click()

        # Esperar un poco a que se carguen los resultados
        time.sleep(2)

        # Extraer el modelo del coche (asegúrate de que el selector es correcto)
        modelo_elemento = driver.find_element(By.CSS_SELECTOR, ".resultado-modelo")  # Cambia el selector al correcto
        modelo = modelo_elemento.text
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        modelo = "Modelo no encontrado"
    
    finally:
        # Cerrar el navegador
        driver.quit()

    return modelo
