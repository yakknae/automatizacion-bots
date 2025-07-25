# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configurar la carpeta de descargas
download_folder = os.path.abspath("downloads")
os.makedirs(download_folder, exist_ok=True)
chrome_profile_path = r"C:\Users\valen\AppData\Local\Google\Chrome\User Data"

# Configurar opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("--profile-directory=Default")  # o "Profile 1", etc.
options.add_experimental_option("detach", True)


# Iniciar el navegador
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # --- PASO 1: Abrir Gmail ---
    driver.get("https://mail.google.com/ ")
    print("🔹 Abriendo Gmail...")
    time.sleep(5)  # Espera a que cargue o inicies sesión manualmente

    # ⚠️ NOTA: Deja que inicies sesión manualmente (opcional)
    input("✅ Presiona ENTER después de iniciar sesión en Gmail...")

    # --- PASO 2: Buscar un correo específico ---
    search_box = driver.find_element(By.XPATH, '//input[@aria-label="Buscar"]')
    search_box.clear()
    search_query = "sjabgd"  # Cambia esto por el asunto que buscas
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    print(f"🔍 Buscando correos con: '{search_query}'")
    time.sleep(5)

    # --- PASO 3: Hacer clic en el primer correo que coincida ---
    try:
        # Busca un correo que contenga el texto del asunto
        first_email = driver.find_element(
            By.XPATH, f'//span[contains(text(), "{search_query}") or contains(@name, "{search_query}")]'
        )
        first_email.click()
        print("📧 Correo abierto.")
        time.sleep(3)
    except Exception as e:
        print("❌ No se encontró ningún correo con ese asunto.")
        raise e

    # --- PASO 4: Buscar y hacer clic en el botón de descarga ---
    try:
        # El botón de descarga tiene aria-label="Descargar"
        download_button = driver.find_element(By.XPATH, '//div[@aria-label="Descargar"]')
        download_button.click()
        print("⬇️ Archivo descargado.")
    except Exception as e:
        print("📎 No se encontró un archivo adjunto para descargar.")
        # Puede que no haya adjuntos

    time.sleep(5)  # Espera a que termine la descarga

finally:
    print(f"📁 Los archivos se han descargado en: {download_folder}")
    # No cerramos el navegador inmediatamente para revisar
    # Si quieres cerrarlo automáticamente, descomenta:
    # driver.quit()