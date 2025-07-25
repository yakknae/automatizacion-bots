import webbrowser
import pyautogui
import time
import cv2
import numpy as np
import os
import pandas as pd
import logging
import pyperclip

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("automatizacion.log", encoding='utf-8'),  # Guarda en archivo
                    logging.StreamHandler()])


class FinalFantasy:
    def __init__(self):
        self.direccion = ""
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        logging.info("--------------------- BOT INICIADO ---------------------")

    def abrir_navegador(self):
        try:
            logging.info("Abriendo navegador")
            webbrowser.open("https://www.google.com ")
            time.sleep(2)
            logging.info("Navegador abierto")
        except Exception as e:
            logging.error(f"Error al abrir el navegador: {e}")
    
    def escribir_direccion(self,direccion):
        self.direccion = direccion
    
    def limpiar_barra(self):
        try:
            logging.info("Limpiando la barra de busqueda del navegador...")
            # seleccionar la barra de navegacion (Ctrl + L)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            # seleccionar lo que haya en la borra (Ctrl + L)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            # borrar lo que haya en la barra de navegacion (Ctrl + L)
            pyautogui.hotkey('ctrl', 'delete')
            time.sleep(0.3)
        except Exception as e:
            logging.error(f"Erorr al limpiar la barra de busqueda del navegador: {e}")
        


    def buscar_direccion(self):
        if not self.direccion:
            print("no hay una direccion")
            return

        try:
            self.limpiar_barra()
            logging.info("Escribiendo direccion...")
            # escribir direccion
            pyautogui.write(self.direccion, interval=0.1)
            time.sleep(0.5)

            # buscar direccion
            pyautogui.press('enter')
        except Exception as e:
            logging.error(f"Error al buscar la direccion: {e}")


    def scroll(self,cantidad):
            try:
                logging.info("Scroll...")
                pyautogui.scroll(cantidad)
                time.sleep(0.3)
            except Exception as e:
                logging.error(f"Error al hacer scroll: {e}")

    def mouseMid(self):
        try:
            # Obtener tamaño de la pantalla
            screen_width, screen_height = pyautogui.size()
            
            # Calcular el centro
            center_x = screen_width // 2
            center_y = screen_height // 2

            # Mover el mouse al centro
            pyautogui.moveTo(center_x, center_y)
            logging.info("Mouse movido al centro:")
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Error al mover el mouse al medio de la pantalla: {e}")

    def tomar_foto(self, filename="captura.png"):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"Captura guardada como {filename}")
            logging.info(f"captura guardada como: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error al tomar captura: {e}")
            return None
    
    def buscar_imagen_en_pantalla(self, imagen_buscar, confidence=0.8):
        try:
            plantilla = cv2.imread(imagen_buscar, 0)
            if plantilla is None:
                logging.error(f"No se encontró la imagen: {imagen_buscar}")
                return None

            # Tomar captura
            captura_path = self.tomar_foto()
            if not captura_path:
                return None
            pantalla = cv2.imread(captura_path, 0)

            # Buscar coincidencia
            resultado = cv2.matchTemplate(pantalla, plantilla, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

            # max_val es el nivel de confianza de la mejor coincidencia
            if max_val >= confidence:
                centro_x = max_loc[0] + int(plantilla.shape[1] / 2)
                centro_y = max_loc[1] + int(plantilla.shape[0] / 2)
                logging.info(f"✅ Imagen encontrada con confianza {max_val:.3f} en ({centro_x}, {centro_y})")
                return centro_x, centro_y
            else:
                logging.warning(f"❌ No se encontró coincidencia. Máxima confianza: {max_val:.3f} < {confidence}")
                return None

        except Exception as e:
            logging.error(f"Error al buscar imagen en pantalla: {e}")
            return None

    def hacer_clic_en_imagen(self, ruta_imagen, confidence=0.8):
        try:
            logging.info(f"Buscando imagen con confianza {confidence}: {ruta_imagen}")

            # Buscar centro de la imagen
            location = pyautogui.locateCenterOnScreen(
                ruta_imagen,
                confidence=confidence
            )

            if location:
                x, y = location
                pyautogui.moveTo(x, y)
                time.sleep(0.5)
                pyautogui.click()
                logging.info(f"✅ Clic realizado en ({x}, {y})")
                return True
            else:
                logging.warning(f"❌ No se encontró la imagen: {ruta_imagen}")
                return False

        except Exception as e:
            logging.error(f"❌ Error al hacer clic en imagen: {e}")
            return False           

    def encontrar_archivo_descarga(self, extension=".xlsx"):
        try:
            archivos = []
            for f in os.listdir(self.download_folder):
                if f.endswith(extension):
                    archivos.append(f)

            if not archivos:
                print("no se encontro archivos .xlsx")
                logging.warning("No se encontraron archivos con la extensión especificada.")
                return None
            

            # Ordenar por fecha de modificación (el más reciente primero)
            archivos.sort(key=lambda x: os.path.getmtime(os.path.join(self.download_folder, x)), reverse=True)

            archivo_reciente = os.path.join(self.download_folder, archivos[0])
            print(f" Archivo encontrado: {archivo_reciente}")
            logging.info(f"Archivo encontrado: {archivo_reciente}")
            return archivo_reciente
        except Exception as e:
            logging.error(f"Error al buscar archivo descargado: {e}")
            return None

    def modificar_excel(self,ruta_archivo,nueva_columna="", valor=""):
        try:
            df = pd.read_excel(ruta_archivo)
            print(f"Datos originales:\n{df.head()}")
            logging.info(f"Datos originales:\n{df.head()}")
            #agregar nueva columna
            df[nueva_columna] = valor
            #guardar cambios
            archivo_modificado = ruta_archivo.replace(".xlsx","_modificado.xlsx")
            df.to_excel(archivo_modificado,index=False)
            print(f" Archivo modificado guardado como: {archivo_modificado}")
            logging.info(f"Archivo modificado guardado: {archivo_modificado}")
            return archivo_modificado
        except Exception as e:
            print(f"error al modificar el archivo {e}")
            return None

    def enviar_a_destinatario(self, destinatario, asunto, mensaje, ruta_adjunto):
        try:
            # Hacer clic en "Redactar"
            if not self.hacer_clic_en_imagen("assets/gmail_assets/redactar.png"):
                logging.error("No se encontró el botón de redactar.")
                return False
            time.sleep(2)

            # Escribir destinatario
            pyperclip.copy(destinatario)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('tab')  # Al asunto

            # Asunto
            pyautogui.write(asunto,interval=0.2)
            time.sleep(2)
            pyautogui.press('tab')  # Al cuerpo

            # Mensaje
            pyperclip.copy(mensaje)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)

            # Adjuntar
            if not self.hacer_clic_en_imagen("assets/gmail_assets/adjunto.png"):
                logging.error("No se encontró el botón de adjuntar.")
                return False
            time.sleep(3)

            pyautogui.write(ruta_adjunto)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)

            # Enviar
            if not self.hacer_clic_en_imagen("assets/gmail_assets/enviar.png"):
                logging.error("No se encontró el botón de enviar.")
                return False

            logging.info(f"✅ Correo enviado a: {destinatario}")
            return True

        except Exception as e:
            logging.error(f"Error al enviar correo: {e}")
            return False


if __name__ == "__main__":
    try:
        bot = FinalFantasy()
        bot.abrir_navegador()
        time.sleep(3)
        bot.escribir_direccion("https://mail.google.com/ ")
        bot.buscar_direccion()
        time.sleep(4)
        pyautogui.press('tab')
        time.sleep(2)
        bot.hacer_clic_en_imagen("assets/gmail_assets/buscar.png")
        time.sleep(4)
        pyautogui.write('prueba galleta ')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(5)
        bot.hacer_clic_en_imagen("assets/gmail_assets/grece1.png")
        time.sleep(4)
        for _ in range(6):
            pyautogui.press('tab')
        time.sleep(4)
        pyautogui.press('enter')
        time.sleep(4)
        for _ in range(2):
            pyautogui.press('esc')
        time.sleep(2)
        archivo_excel = bot.encontrar_archivo_descarga(extension=".xlsx")
        pyautogui.press('esc')
        time.sleep(4)
        pyautogui.press('esc')
        if archivo_excel:
           archivo_modificado = bot.modificar_excel(archivo_excel,nueva_columna="estado",valor="automatizado") 
           if archivo_modificado:
                 bot.enviar_a_destinatario(
                    destinatario="grecekore@gmail.com",
                    asunto="Excel galleta",
                    mensaje="Hola, aquí está el archivo actualizado.",
                    ruta_adjunto=archivo_modificado
                )
        else:
            logging.warning("No se encontró el archivo Excel descargado.")
    except Exception as e:
        logging.critical(f"Error crítico en el flujo principal: {e}")
