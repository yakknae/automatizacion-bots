import webbrowser
import pyautogui
import time
import cv2
import numpy as np
import os

class FinalFantasy:
    def __init__(self):
        self.direccion = ""
    
    def abrir_navegador(self):
        webbrowser.open("https://www.google.com ")
        time.sleep(2)
    
    def escribir_direccion(self,direccion):
        self.direccion = direccion
    
    def limpiar_barra(self):
        # seleccionar la barra de navegacion (Ctrl + L)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        # seleccionar lo que haya en la borra (Ctrl + L)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        # borrar lo que haya en la barra de navegacion (Ctrl + L)
        pyautogui.hotkey('ctrl', 'delete')
        time.sleep(0.3)

    def buscar_direccion(self):
        if not self.direccion:
            print("no hay una direccion")
            return

        self.limpiar_barra()

        # escribir direccion
        pyautogui.write(self.direccion, interval=0.1)
        time.sleep(0.5)

        # buscar direccion
        pyautogui.press('enter')

    def scroll(self,cantidad):
            pyautogui.scroll(cantidad)
            time.sleep(0.3)

    def mouseMid(self):
        # Obtener tamaño de la pantalla
        screen_width, screen_height = pyautogui.size()
        
        # Calcular el centro
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Mover el mouse al centro
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.5)

    def tomar_foto(self, filename="captura.png"):
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Captura guardada como {filename}")
        return filename
    
    def buscar_imagen_en_pantalla(self, imagen_buscar, umbral=0.8):
        plantilla = cv2.imread(imagen_buscar,0)
        pantalla = cv2.imread(self.tomar_foto(),0)
        if plantilla is None:
            print(f"no se encontro la foto a buscar: {imagen_buscar}")
            return None
        
        resultado = cv2.matchTemplate(pantalla, plantilla, cv2.TM_CCOEFF_NORMED)
        umbral_match = umbral
        loc = np.where(resultado >= umbral_match)

        pt = None
        for pt in zip(*loc[::-1]):  # Obtenemos la primera coincidencia
            break

        if pt is not None:
            # Coordenadas centrales de la imagen encontrada
            centro_x = pt[0] + int(plantilla.shape[1]/2)
            centro_y = pt[1] + int(plantilla.shape[0]/2)
            print(f"Imagen encontrada en ({centro_x}, {centro_y})")
            return centro_x, centro_y
        else:
            print("No se encontró coincidencia.")
            return None

    def hacer_clic_en_imagen(self, ruta_imagen):
        posicion = self.buscar_imagen_en_pantalla(ruta_imagen)
        if posicion:
            x,y = posicion
            pyautogui.moveTo(x,y)
            time.sleep(0.5)
            pyautogui.click()
            print("click hecho")
        else:
            print("No se puede hacer clic, imagen no encontrada.")

        


if __name__ == "__main__":
    bot = FinalFantasy()
    bot.abrir_navegador()
    bot.escribir_direccion("https://www.faceit.com/es/players/viel ")
    bot.buscar_direccion()
    time.sleep(6)
    bot.hacer_clic_en_imagen("assets/estadisticas.png")
    time.sleep(6)
    bot.scroll(cantidad=-2000)
    time.sleep(6)
    bot.hacer_clic_en_imagen("assets/mapa1.png")
    time.sleep(6)
    bot.hacer_clic_en_imagen("assets/general.png")
    time.sleep(6)
    bot.mouseMid()
    time.sleep(2)
    bot.scroll(cantidad=-1000)
