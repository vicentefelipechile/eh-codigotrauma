# ============================================================
# Importar librerias
# ============================================================

import os
import sys
import json
import pathlib

# ============================================================
# Obtener la configuracion del proyecto en "./config.json"
# ============================================================

MAIN_PATH: str = str(pathlib.Path(__file__).parent.parent.absolute()) + "/"
Configuracion: dict = None

try:
    with open(MAIN_PATH + './config.json', 'r') as Configuracion:
        Configuracion: dict = json.load(Configuracion)
except FileNotFoundError:
    print("=====================================")
    print("No se ha encontrado el archivo de configuracion")
    print("=====================================")

    exit()

# ============================================================
# Verificar que esta instalado django en el entorno virtual
# ============================================================

try:
    import django
except ImportError:
    print("=====================================")
    print("No se ha encontrado Django instalado")
    print("Instalando Django...")
    print("=====================================")

    # Nuevo formato utilizando MAIN_PATH
    print(f" > {sys.executable} -m pip install -r {MAIN_PATH}requirements.txt")
    os.system(f'{sys.executable} -m pip install -r {MAIN_PATH}requirements.txt')

print("=====================================")
print("Caracteristicas necesarias instaladas")
print("Iniciando proyecto...")
print("")

try:
    # Migrar aplicaciones

    # Nuevo formato utilizando MAIN_PATH
    print(f' > python {MAIN_PATH}manage.py migrate')
    os.system(f'python {MAIN_PATH}manage.py migrate')

    if Configuracion["alwaysOpenBrowser"]:
        print(f' > python -m webbrowser "http://127.0.0.1:8000"')
        os.system(f'python -m webbrowser "http://127.0.0.1:8000"') 

    print("")
    print(f' > python {MAIN_PATH}manage.py runserver')

    print("=====================================")
    os.system(f'python {MAIN_PATH}manage.py runserver')

except KeyboardInterrupt:
    print("=====================================")
    pass
except Exception as Error:
    print("=====================================")
    print("Error al iniciar el proyecto")
    print("")
    print(Error)
    print("")
    print("Terminando...")
    print("=====================================")
    print("")

    exit()