# ============================================================
# Importar librerias
# ============================================================

import os
import sys
import json
import pathlib
from shutil import rmtree

# ============================================================
# Clase Principal
# ============================================================

class Main:

    # Variables
    Configuracion: dict = None
    TipoDeEjecucion: dict = {}
    MAIN_PATH: str = str(pathlib.Path(__file__).parent.parent.absolute()) + "\\"


    # ============================================================
    # Inicializar
    # ============================================================

    def NormalEjecucion(self: object) -> None:
        try:
            with open(self.MAIN_PATH + './root/config.json', 'r') as Configuracion:
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

            # Nuevo formato utilizando self.MAIN_PATH
            print(f" > {sys.executable} -m pip install django")
            os.system(f"{sys.executable} -m pip install django")

        print("=====================================")
        print("Caracteristicas necesarias instaladas")
        print("Iniciando proyecto...")
        print("")

        try:
            # Migrar aplicaciones

            # Nuevo formato utilizando self.MAIN_PATH
            print(f' > python {self.MAIN_PATH}manage.py migrate')
            os.system(f'python {self.MAIN_PATH}manage.py migrate')

            if Configuracion["alwaysOpenBrowser"]:
                print(f' > python -m webbrowser "http://127.0.0.1:8000"')
                os.system(f'python -m webbrowser "http://127.0.0.1:8000"') 

            print("")
            print(f' > python {self.MAIN_PATH}manage.py runserver')

            print("=====================================")
            os.system(f'python {self.MAIN_PATH}manage.py runserver')

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

            os.system("pause")
            exit()


    # ============================================================
    # Tipo de ejecucion
    # ============================================================

    def restaurar(self: object) -> None:
        # Eliminar el archivo "db.sqlite3" en ./

        print("Eliminando base de datos...")
        print(f" > del {self.MAIN_PATH}db.sqlite3")
        if ( os.path.exists(self.MAIN_PATH + "db.sqlite3") ):
            os.remove(self.MAIN_PATH + "db.sqlite3")

        print("Eliminando migraciones...")
        print(f" > rmdir /s /q {self.MAIN_PATH}principal/migrations")
        if ( os.path.exists(self.MAIN_PATH + "principal/migrations") ):
            rmtree(self.MAIN_PATH + "principal/migrations")


    def ayuda(self: object) -> None:
        print(f"""                Ayuda
=====================================

Este codigo esta creado con el proposito de administrar
el proyecto de Django de la forma mas sencilla posible.

Argumentos disponibles:
    > ayuda  
    > restaurar""")


    # ============================================================
    # Ejecucion Avanzada
    # ============================================================

    def EjecucionEspecial(self: object, Argumentos: list = None) -> None:
        Tipo: str = Argumentos[1]

        print("=====================================")
        if hasattr(self, Tipo):
            getattr(self, Tipo)()
        else:
            print("No se ha encontrado la funcion")

        print("=====================================")
        exit()



# ============================================================
# Obtener argumentos
# ============================================================

# Si el archivo se ejecuto sin argumentos entonces ejecuta la funcion NormalEjecucion
if __name__ == '__main__':
    if len(sys.argv) == 1:
        Main().NormalEjecucion()
    else:
        Main().EjecucionEspecial(sys.argv)