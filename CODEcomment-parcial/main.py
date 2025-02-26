from kivy.app import App
from functools import partial
from kivy.uix.spinner import Spinner
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import platform
import os, sys
import json
import string
import psutil
import subprocess


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """ ##accion necesaria para carga de imagen seguras
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



##ARRAYS==LOGIN/REGISTER

info_sistema = {}
usuarios = {}

def guardar_datos_usuarios(datos): #Guarda datos
    try:
        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo)
    except Exception as e:
        print("Error al guardar datos de usuarios:", e)
 
def cargar_datos_usuarios(): #Carga datos
    try:
        with open("usuarios.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error al cargar datos de usuarios:", e)
        return {}



class Zembra(App): #Clase main
    def build(self,):  #Build pantallas
        juegos_especificaciones = {}
        Window.size = (800, 600)
        self.title = "Zembra-Prototype"
        self.orientation = "vertical"
        layout = BoxLayout(orientation='vertical')
##INICIO PANTALLA
        self.layout = BoxLayout(orientation="vertical", spacing=40, padding=60)
        with self.layout.canvas.before:
            self.background = Rectangle(source=resource_path('fondo.png'), pos=(0, 0), size=(800, 600))
        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image) #imagen usadas de fondo y nombre

        self.label = Label(text="¡Bienvenido a Zembra!", font_size=16, bold=True)
        self.layout.add_widget(self.label)

        self.username_input = TextInput(hint_text="Usuario")
        self.layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Contraseña", password=True)
        self.layout.add_widget(self.password_input)

        self.registrar_btn = Button(text="Registrar",background_color = (128, 0, 128) ,background_normal = '',bold = True, on_press=self.registrar)
        self.layout.add_widget(self.registrar_btn)

        self.iniciar_sesion_btn = Button(text="Iniciar Sesion",background_color = (128, 0, 128),background_normal = '',bold = True, on_press=self.iniciar_sesion)
        self.layout.add_widget(self.iniciar_sesion_btn)

        return self.layout


##INICIO REGISTRO


    def tiene_caracter_especial(self, contrasena):  #genera y detecta caracteres especiales
        caracteres_especiales = string.punctuation
        return any(char in caracteres_especiales for char in contrasena)

    def registrar(self, instance):  #funcion de registro
        try:
            nombre_usuario = self.username_input.text
            contrasena = self.password_input.text

            if nombre_usuario in usuarios:
                self.label.text = "El nombre de usuario ya está registrado. Por favor, intenta con otro."
            elif len(contrasena) < 8:
                self.label.text = "La contraseña debe tener al menos 8 caracteres. Por favor, intenta con otra."
            elif not self.tiene_caracter_especial(contrasena):
                self.label.text = "La contraseña debe contener al menos un carácter especial. Por favor, agregale."
            else:
                usuarios[nombre_usuario] = contrasena
                guardar_datos_usuarios(usuarios)
                self.label.text = "¡Registro exitoso! Ahora puedes iniciar sesión."

        except Exception as e:
            self.label.text = "Ocurrió un error al registrar el usuario. Por favor, intenta nuevamente."
            print("Error al registrar usuario:", e)


    def iniciar_sesion(self, instance): #funcion de inicio de sesion
        try:
            nombre_usuario = self.username_input.text
            contrasena = self.password_input.text

            if nombre_usuario in usuarios and usuarios[nombre_usuario] == contrasena:
                self.label.text = f"Bienvenido, {nombre_usuario}!"
                self.username_input.text = ""
                self.password_input.text = ""
                self.mostrar_pantalla_interactiva()
            else:
                self.label.text = "Nombre de usuario o contraseña incorrectos. Por favor, intenta nuevamente."

        except Exception as e:
            self.label.text = "Ocurrió un error al iniciar sesión. Por favor, intenta nuevamente."
            print("Error al iniciar sesión:", e)

##FIN REGISTRO

##PANTALLA INTERACTIVA

    def mostrar_pantalla_interactiva(self, *args):  #pantalla main de interactividad
        self.layout.clear_widgets()

        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image)

        self.label = Label(text="¿En que podemos ayudarte?", font_size=16, bold=True)
        self.layout.add_widget(self.label)

        self.btn_scanner = Button(text="Escanea tu computador", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=partial(self.scanner))
        self.layout.add_widget(self.btn_scanner)

        self.btn_selector = Button(text="Selector de juego", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=partial(self.selector))
        self.layout.add_widget(self.btn_selector)

        self.btn_comparacion = Button(text="Comparacion de componentes", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=partial(self.comparar_componentes))
        self.layout.add_widget(self.btn_comparacion)
        
        self.btn_tres = Button(text="Consultar con Administración", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=partial(self.administracion))
        self.layout.add_widget(self.btn_tres)

        self.btn_cerrar_aplicacion = Button(text="Cerrar Zembra", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=partial(self.cerrar_aplicacion))
        self.layout.add_widget(self.btn_cerrar_aplicacion)
        

        return self.layout



##BUILD PANTALLA INTERACTIVA

    def scanner(self, *args):  #funcion de escaner
        self.layout.clear_widgets()
        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image)

        self.display_information("Información del Sistema: ", align="center", font_size=12, bold=True)
        self.obtener_informacion_sistema()
        self.display_information("\nInformación de la CPU: ", font_size=12, bold=True)
        self.obtener_informacion_cpu()
        self.display_information("\nInformación de la Memoria: ", font_size=12, bold=True)
        self.obtener_informacion_memoria()
        self.display_information("Información Tarjeta Grafica:\n", font_size=12, bold=True)
        self.obtener_informacion_tarjeta_grafica()  ##display para mostrar en pantalla

        self.btn_volver = Button(text="Volver", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)
    

    def obtener_informacion_sistema(self):  #main de obtencion
        sistema_operativo = platform.system()
        version_sistema = platform.version()
        arquitectura_sistema = platform.architecture()

        info_text = f"Versión del Sistema:{sistema_operativo, version_sistema}\n" \
                    f"Arquitectura del Sistema: {arquitectura_sistema}"
        self.display_information(info_text)
        

    def obtener_informacion_cpu(self):  #scan cpu
        cpu_info = platform.processor()
        num_cores = psutil.cpu_count(logical=False)
        num_threads = psutil.cpu_count(logical=True)

        info_text = f"Procesador: {cpu_info}\n" \
                    f"Número de Cores: {num_cores}\n" \
                    f"Número de Hilos: {num_threads}\n"
        self.display_information(info_text)

    def obtener_informacion_memoria(self): #scan memory
        memoria_total = psutil.virtual_memory().total / (1024 ** 3)
        info_text = f"Memoria Total: {memoria_total:.2f} GB"
        self.display_information(info_text)

    def obtener_informacion_tarjeta_grafica(self):  #scan tarjeta grafica con calculos al igual que el resto
        sistema_operativo = platform.system()

        if sistema_operativo == "Windows":
            try:
                resultado = subprocess.check_output("wmic path win32_videocontroller get caption\n", shell=True, text=True)
                info_text = f"\n{resultado}"
                self.display_information(info_text)
            except Exception as e:
                print(f"Error al obtener información de la Tarjeta Gráfica:\n {e}")
        elif sistema_operativo == "Linux":
            try:
                resultado = subprocess.check_output("lspci | grep VGA", shell=True, text=True)
                info_text = f"Información de la Tarjeta Gráfica (Linux):\n{resultado}"
                self.display_information(info_text)
                resultado_adicional = subprocess.check_output("lshw -C display", shell=True, text=True)
                info_text_adicional = f"Características Adicionales de la Tarjeta Gráfica (Linux):\n{resultado_adicional}"
                self.display_information(info_text_adicional)
            except Exception as e:
                print(f"Error al obtener información de la Tarjeta Gráfica: {e}")
        else:
            info_text = "La obtención de información de la Tarjeta Gráfica no es compatible en este sistema operativo.\n"
            self.display_information(info_text)
    
    def display_information(self, text, align="center", font_size=14, bold=True): #main de display
        if text is not None:
            label = Label(text=str(text), font_size=font_size, halign=align, bold=bold)
            self.layout.add_widget(label)
        else:
            print("Intento de mostrar información nula. Texto:", text)



##ADMINISTRACION


    def administracion(self,*args, align="center", font_size=16, bold=True):  #sector de administracion 
        self.layout.clear_widgets()
        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image)
        self.text_label = Label(text="Para contactarte con un administrador o resolver una duda: \nzembraconsult@gmail.com\n11-4243-5531\nAvenida siempre viva n°123", font_size=font_size, halign=align, bold=bold)
        self.layout.add_widget(self.text_label)
        image = Image(source=resource_path('messi.jpeg'), size_hint=( 1, 6))
        self.layout.add_widget(image)
        self.campeon_label = Label(text="¡A todo esto, un año del momento mas bonito!\nAutores: Moreno Thomas - Medina Nehuen\nGutierrez Facundo - Pereyra Brandon\nMiqueas Francisco - Martinez Juan", font_size=font_size, halign=align, bold=bold)
        self.layout.add_widget(self.campeon_label)
        self.btn_volver = Button(text="Volver", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)

##SELECTOR GAME

    def selector(self, *args): #funcion de selector de requisito minimo
        self.layout.clear_widgets()

        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image)

        self.juegos_especificaciones = {
            "League of Legends": ["Intel Core i3-530", "A6-3650", "GeForce 9600GT", "HD 6570", "RAM: 2 GB"],
            "Valorant": ["Intel Core 2 Duo E8400", "AMD Athlon 200GE", "Intel HD 4000", "AMD Radeon R5 200", "RAM: 4 GB"],
            "FIFA 24": ["Intel Core i5-6600K 3.50GHz", "AMD Ryzen 5 1600 3.2 GHz", "NVIDIA GeForce GTX 1050 Ti 4GB", "AMD Radeon RX 570 4GB", "RAM: 8 GB"],
            "Call of Duty": ["Intel Core i5-6600", "AMD Ryzen 5 1400", "NVIDIA GeForce GTX 960", "GTX 1650", "AMD Radeon RX 470", "RAM: 8 GB"],
            "Counter Strike": ["Intel Core 2 Duo E6600", "AMD Phenom™ X3 8750", "most be 256 MB", "RAM: 2GB"],
            "Minecraft": ["Intel Pentium D", "AMD Athlon 64", "Nvidia GeForce 9600 GT", "AMD Radeon HD 2400", "RAM: 2GB"],
            "GTA V": ["Intel Core 2 Quad CPU Q6600", "AMD Phenom 9850 Quad-Core", "NVIDIA 9800 GT 1GB", "AMD HD 4870 1GB", "RAM: 4GB"],
            "Fortnite": ["Intel Core i3-3225","AMD Athlon II X2", "Intel HD 4000", "AMD Radeon Vega 8", "RAM: 8GB"],
        }  #carga de juegos

        self.spinner = Spinner(text='League of Legends', background_color = (128, 0, 128),background_normal = '',bold = True, values=list(self.juegos_especificaciones.keys()))
        self.layout.add_widget(self.spinner) #spiner para crear la interactividad

        self.label = Label(text='\n'.join(self.juegos_especificaciones['League of Legends']))
        self.layout.add_widget(self.label)

        self.button = Button(text='Mostrar Especificaciones', background_color = (128, 0, 128),background_normal = '',bold = True,)
        self.button.bind( on_press=self.mostrar_especificaciones)
        self.layout.add_widget(self.button)

        self.btn_volver = Button(text="Volver", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver) #funcion de volver

        return self.layout
    def mostrar_especificaciones(self, instance): #para que muestre especificaciones /join para la interaccion
        juego_seleccionado = self.spinner.text
        especificaciones = self.juegos_especificaciones.get(juego_seleccionado, ["Especificaciones no encontradas"])
        self.label.text = '\n'.join(especificaciones)

##COMPARACION CORRECCIONES

    def comparar_componentes(self, *args):  #comparacion de componentes
        self.layout.clear_widgets()

        self.image = Image(source=resource_path('zembra.png'))
        self.layout.add_widget(self.image)

        self.juegos_especificaciones = {
            "League of Legends": ["Intel Core i3-530", "A6-3650", "GeForce 9600GT", "HD 6570", "RAM: 2 GB"],
            "Valorant": ["Intel Core 2 Duo E8400", "AMD Athlon 200GE", "Intel HD 4000", "AMD Radeon R5 200", "RAM: 4 GB"],
            "FIFA 24": ["Intel Core i5-6600K 3.50GHz", "AMD Ryzen 5 1600 3.2 GHz", "NVIDIA GeForce GTX 1050 Ti 4GB", "AMD Radeon RX 570 4GB", "RAM: 8 GB"],
            "Call of Duty": ["Intel Core i5-6600", "AMD Ryzen 5 1400", "NVIDIA GeForce GTX 960", "GTX 1650", "AMD Radeon RX 470", "RAM: 8 GB"],
            "Counter Strike": ["Intel Core 2 Duo E6600", "AMD Phenom™ X3 8750", "most be 256 MB", "RAM: 2GB"],
            "Minecraft": ["Intel Pentium D", "AMD Athlon 64", "Nvidia GeForce 9600 GT", "AMD Radeon HD 2400", "RAM: 2GB"],
            "GTA V": ["Intel Core 2 Quad CPU Q6600", "AMD Phenom 9850 Quad-Core", "NVIDIA 9800 GT 1GB", "AMD HD 4870 1GB", "RAM: 4GB"],
            "Fortnite": ["Intel Core i3-3225","AMD Athlon II X2", "Intel HD 4000", "AMD Radeon Vega 8", "RAM: 8GB"],
        }

        self.spinner = Spinner(text='League of Legends', background_color = (128, 0, 128),background_normal = '',bold = True,  values=list(self.juegos_especificaciones.keys()))
        self.layout.add_widget(self.spinner)

        self.display_information("\nComparación de Componentes: ", font_size=12, bold=True)

        self.comparar_y_mostrar_componentes()

        self.btn_volver = Button(text="Volver", background_color = (128, 0, 128),background_normal = '',bold = True, on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)

    def comparar_y_mostrar_componentes(self):
        juego_seleccionado = self.spinner.text
        especificaciones_juego = self.juegos_especificaciones.get(juego_seleccionado, [])

        if especificaciones_juego:
            resultado_comparacion = self.realizar_comparacion(especificaciones_juego)
            self.display_information(resultado_comparacion)
        else:
            self.display_information("No se encontraron especificaciones para el juego seleccionado.")
    def realizar_comparacion(self, especificaciones_juego):
        comparacion = []

        info_cpu = self.obtener_informacion_cpu()
        info_memoria = self.obtener_informacion_memoria()
        info_tarjeta_grafica = self.obtener_informacion_tarjeta_grafica()

        #CPU
        if info_cpu and self.comparar_cpu(info_cpu, especificaciones_juego):   #aca con un simple bucle se hace la comparativa y en el resto igual
            comparacion.append("CPU: Las especificaciones del juego son compatibles.")
        else:
            comparacion.append("CPU: Las especificaciones del juego no son compatibles.")

        ##Memoria RAM
        if info_memoria and any(memoria_info in info_memoria for memoria_info in especificaciones_juego):
            comparacion.append("Memoria: Las especificaciones del juego son compatibles.")
        else:
            comparacion.append("Memoria: Las especificaciones del juego no son compatibles.")

        ##Tarjeta Gráfica
        if info_tarjeta_grafica and any(grafica_info in info_tarjeta_grafica for grafica_info in especificaciones_juego):
            comparacion.append("Tarjeta Gráfica: Las especificaciones del juego son compatibles.")
        else:
            comparacion.append("Tarjeta Gráfica: Las especificaciones del juego no son compatibles.")
        
        ##Calificacion de gama
        if all("¡Cumple!" in mensaje for mensaje in comparacion):
            comparacion.append("¡La PC es de mayor gama!")
        else:
            comparacion.append("La PC es de menor gama.")

        return '\n'.join(comparacion)

    def comparar_cpu(self, info_cpu, especificaciones_juego):  #para las especificaciones se hace esta funcion con los nombres comerciales
        palabras_clave_cpu = set(info_cpu.lower().split())
        palabras_clave_juego = set(especificacion.lower() for especificacion in especificaciones_juego)

        if palabras_clave_cpu.intersection(palabras_clave_juego):
            return True

        return False
    
##ACA TERMINA LA ZONA DE COMPARACIONES

##CIERRE APP

    def cerrar_aplicacion(self,intance,*args): #cierre de la app funcion
        self.stop()

##Fin

if __name__ == "__main__":
    try:
        usuarios = cargar_datos_usuarios()
        Zembra().run()
    except Exception as e:
        print("Error al ejecutar la aplicación:", e)
