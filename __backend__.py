# ============================================================
# Importar librerias
# ============================================================

import os
import sys
import json

# ============================================================
# Obtener la configuracion del proyecto en "./config.json"
# ============================================================

try:
    with open('./config.json', 'r') as Configuracion:
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
    print("=====================================")

    # Intentar instalar django
    print("=====================================")
    print("Instalando Django...")
    print("=====================================")

    import os
    import sys

    print(f"{sys.executable} -m pip install django")
    os.system(f'{sys.executable} -m pip install django')

print("=====================================")
print("Caracteristicas necesarias instaladas")
print("")
print("Iniciando proyecto...")
print("=====================================")

try:
    # Migrar aplicaciones
    print(f'python {Configuracion["backend"]["MAIN_PATH"]}manage.py migrate')
    os.system(f'python {Configuracion["backend"]["MAIN_PATH"]}manage.py migrate')

    if Configuracion["alwaysOpenBrowser"]:
        print(f'python -m webbrowser "http://127.0.0.1:8000"')
        os.system(f'python -m webbrowser "http://127.0.0.1:8000"') 


    print(f'python {Configuracion["backend"]["MAIN_PATH"]}manage.py runserver')
    print("=====================================")
    os.system(f'python {Configuracion["backend"]["MAIN_PATH"]}manage.py runserver')
except KeyboardInterrupt:
    pass
except Exception as Error:
    print("=====================================")
    print("Error al iniciar el proyecto")
    print("=====================================")
    print("")
    print(Error)
    print("")
    print("=====================================")
    print("Terminando...")
    print("=====================================")
    print("")

    exit()