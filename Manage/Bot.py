from Manage.Driver import CompDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import os
import requests
import zipfile
import time
import tempfile


class CompBot:
    def __init__(self, dirs):
        self.__dirs = dirs
        self.__carpeta = dirs.get_output_doc()
        self.__driver = CompDriver.get_driver(self.__carpeta)

        self.__url = dirs.get_url()
        self.__input = dirs.get_input()
        self.__ouput = dirs.get_output()

    def login(self):
        self.__driver.get(self.__url)
        WebDriverWait(self.__driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div")))

    def DescargarArchivo(self):
        ruta_desc = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divMsg"]/div[4]/a')))
        nombre_archivo = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divMsg"]/div[4]/a'))).text
        enlace = ruta_desc.get_attribute('href')
        response = requests.get(enlace, stream=True)

        ruta_zip = os.path.join(self.__carpeta, nombre_archivo)
        with open(ruta_zip, 'wb') as archivo:
            for datos in response.iter_content(chunk_size=1024):
                archivo.write(datos)

    def ConsultarDatos(self, ruta):
        # Seleccionar opcion consulta 100
        btn_opc = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/ul/li[2]/a")))
        btn_opc.click()
        # Campo para set archivo
        time.sleep(3)
        campo_file = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, "txtfile")))
        campo_file.send_keys(ruta)
        # Boton para la consulta
        time.sleep(2)
        btn_consultar = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/form[2]/div[2]/div[1]/button')))
        btn_consultar.click()
        # Espera descarga
        time.sleep(20)
        # Descargar archivo
        self.DescargarArchivo()
        # Boton para volver
        btn_volver = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnBuscarBandAutImp"]')))
        btn_volver.click()
        # Esperar pagina de inicio
        time.sleep(3)
        WebDriverWait(self.__driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div")))

    def contar_bloque_y_listar_rutas(self, ruta_carpeta):
        # Lista para almacenar las rutas completas de los archivos
        rutas_archivos = []
        # Verificar que la ruta de la carpeta existe
        if os.path.exists(ruta_carpeta):
            # Listar todos los archivos en la carpeta
            for archivo in os.listdir(ruta_carpeta):
                # Comprobar si el archivo es un txt y comienza con "bloque"
                if archivo.endswith(".txt") and archivo.startswith("bloque"):
                    # Agregar la ruta completa del archivo a la lista
                    rutas_archivos.append(os.path.join(ruta_carpeta, archivo))
        return rutas_archivos

    def guardar_bloques(self, dataframe, ruta_carpeta):
        # Asegurarse de que la ruta existe
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        # Calcular cuántos archivos serán necesarios
        num_archivos = len(dataframe) // 100 + (1 if len(dataframe) % 100 else 0)

        # Dividir y guardar en bloques de 100 líneas
        for i in range(num_archivos):
            bloque = dataframe.iloc[i * 100:(i + 1) * 100]
            nombre_archivo = f"bloque_{i + 1}.txt"
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            bloque.to_csv(ruta_completa, sep='|', index=False, header=False)

    def listar_archivos_zip(self):
        archivos_zip = []
        for archivo in os.listdir(self.__carpeta):
            if archivo.endswith(".zip"):
                archivos_zip.append(os.path.join(self.__carpeta, archivo))

        return archivos_zip

    def Limpiar_Datos(self, ruta_txt):
        # 1) Cadena a borrar
        secuencia = (
            '                                                                                                             '
        )

        # 2) Creamos un fichero temporal en la misma carpeta
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=ruta_txt.parent,  # misma carpeta
            suffix=".tmp",  # extensión temporal
            text=True  # modo texto
        )
        os.close(tmp_fd)  # Cerramos el descriptor, lo abriremos de forma normal
        try:
            # 3) Leemos el original y escribimos la versión limpia en el tmp
            with ruta_txt.open("r", encoding="utf-8") as f_in, \
                    open(tmp_path, "w", encoding="utf-8") as f_out:
                for linea in f_in:
                    f_out.write(linea.replace(secuencia, ""))

            # 4) Reemplazamos el archivo original por el temporal
            os.replace(tmp_path, ruta_txt)  # atómico en la mayoría de SO
        finally:
            # Si ocurrió un error y el temporal aún existe, lo borramos
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def main(self):
        if os.path.isfile(self.__input):
            # Importamos los datos
            input_doc = pd.read_csv(self.__input, dtype=str, delimiter='|', encoding='latin-1', header=None)
            # Separamos los datos en bloques de 100
            self.guardar_bloques(input_doc, self.__carpeta)

        # Obtenemos una lista con las rutas de los bloques
        list = self.contar_bloque_y_listar_rutas(self.__carpeta)

        # Si hay bloques por validar realizamos la consulta
        if list:
            self.login()
            for ruta in reversed(list):
                self.ConsultarDatos(ruta)
                os.remove(ruta)

        # Extraemos las rutas de los .zip
        lista_zips = self.listar_archivos_zip()

        # Extraemos y juntamos los archivos
        if lista_zips:
            with open(self.__ouput, 'w', encoding='utf-8') as archivo_final:
                for zip in lista_zips:
                    with zipfile.ZipFile(zip, 'r') as archivo_zip:
                        # Extraer todos los archivos en la carpeta de destino
                        archivo_zip.extractall(self.__carpeta)

                        for nombre_archivo in archivo_zip.namelist():
                            ruta_archivo_extraido = os.path.join(self.__carpeta, nombre_archivo)

                            # Usa la codificación UTF-8 para leer el archivo extraído
                            with open(ruta_archivo_extraido, 'r', encoding='utf-8') as archivo_extraido:
                                next(archivo_extraido)  # Saltar la cabecera
                                for linea in archivo_extraido:
                                    archivo_final.write(linea)

                            os.remove(ruta_archivo_extraido)
                    os.remove(zip)

        self.Limpiar_Datos(self.__ouput)
