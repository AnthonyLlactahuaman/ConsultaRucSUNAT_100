# Consulta Masiva de RUCS SUNAT

Este proyecto permite consultar datos de múltiples RUCS en la página de SUNAT. 

## Descripción

La herramienta toma como input un archivo con una lista de RUCS y realiza consultas en la página de SUNAT, que permite hacer consultas en bloques de 100 RUCS. Finalmente, consolida toda la información obtenida en un solo archivo de salida.

---

## Requisitos previos

- Descargar el driver de Selenium de [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) y colocar el ejecutable en la carpeta raíz del proyecto.

---

## Uso

1. Coloca el archivo de entrada llamado `Rucs.txt` dentro de la carpeta `Outputs`.

2. El archivo `Rucs.txt` debe contener los RUCS a consultar con el siguiente formato (cada RUC seguido de una barra vertical `|`):

```

RUC1|
RUC2|
RUC3|

```

3. Ejecuta el script para que inicie las consultas y genere el archivo consolidado.

---

## Estructura de carpetas

```

/ (carpeta raíz)
\|-- Edge.exe
\|-- Outputs/
  \|-- Rucs.txt
\|-- Ouputs/
\|-- Manage/
\|-- main.py
\|-- README.md

```

---

## Notas

- Asegúrate de que el driver de Selenium sea compatible con la versión de tu navegador.
- La herramienta procesa los RUCS de 100 en 100 según la limitación del sitio web SUNAT.
- El archivo de salida consolidado se generará en la carpeta del proyecto (detalles según tu implementación).

---

Si tienes dudas o sugerencias, no dudes en abrir un issue o contactarme.
```
