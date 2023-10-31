# ============================================================
# Importar librerias
# ============================================================

import os
import sys
import json
import pathlib
from shutil import rmtree
from faker import Faker


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
        
        print("=====================================")

        try:
            import django
            print(" > Django instalado")
        except ImportError:
            print("No se ha encontrado Django instalado")
            print("Instalando Django...")

            print(f" > {sys.executable} -m pip install django")
            os.system(f"{sys.executable} -m pip install django")
        
        try:
            import faker
            print(" > Faker instalado")
        except ImportError:
            print("No se ha encontrado Faker instalado")
            print("Instalando Faker...")

            print(f" > {sys.executable} -m pip install faker")
            os.system(f"{sys.executable} -m pip install faker")

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

    def restaurar(self: object, Argumento: any = None) -> None:
        # Eliminar el archivo "db.sqlite3" en ./

        print("Eliminando base de datos...")
        print(f" > del {self.MAIN_PATH}db.sqlite3")
        if ( os.path.exists(self.MAIN_PATH + "db.sqlite3") ):
            os.remove(self.MAIN_PATH + "db.sqlite3")

        print("Eliminando migraciones...")
        print(f" > rmdir /s /q {self.MAIN_PATH}principal/migrations")
        if ( os.path.exists(self.MAIN_PATH + "principal/migrations") ):
            rmtree(self.MAIN_PATH + "principal/migrations")
        
        print("Sincronizando base de datos...")
        print(f" > python {self.MAIN_PATH}manage.py makemigrations")
        os.system(f"python {self.MAIN_PATH}manage.py makemigrations")
        print(f" > python {self.MAIN_PATH}manage.py migrate --run-syncdb")
        os.system(f"python {self.MAIN_PATH}manage.py migrate --run-syncdb")



    def generardatos(self: object, Semilla: str = None) -> None:
        if not Semilla:
            Semilla = "1337"
        
        Resultado: int = 0
        for Caracter in Semilla:
            Resultado += ord(Caracter)
            
        print(f"Semilla: {Resultado}")
        
        Faker.seed(Semilla)
        
        print("Generando datos...")
        
        # Si no existe la carpeta sqlscript la crea
        if not os.path.exists(self.MAIN_PATH + "root/sqlscript"):
            os.mkdir(self.MAIN_PATH + "root/sqlscript")
    
    
    
    def shell(self: object, Argumento: any = None) -> None:
        print("Iniciando shell...")
        print(f" > python {self.MAIN_PATH}manage.py shell")
        os.system(f"python {self.MAIN_PATH}manage.py shell")



    def ayuda(self: object, Argumento: any = None) -> None:
        print(f"""                Ayuda
=====================================

Este codigo esta creado con el proposito de administrar
el proyecto de Django de la forma mas sencilla posible.

Argumentos disponibles:
    > ayuda  
    > restaurar
    > generardatos [Semilla]
    > shell""")
        
    def iniciar(self: object, Argumento: any = None) -> None:
        self.NormalEjecucion()


    # ============================================================
    # Ejecucion Avanzada
    # ============================================================

    def EjecucionEspecial(self: object, Argumentos: list = None) -> None:
        Tipo: str = Argumentos[1]
        Extra: str = Argumentos[2] if len(Argumentos) > 2 else None

        print("=====================================")
        if hasattr(self, Tipo):
            getattr(self, Tipo)(Extra)
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