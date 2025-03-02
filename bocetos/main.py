import json
import base_de_datos
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functools import partial
from kivy.uix.popup import Popup
import platform
import psutil
import subprocess

##ARRAYS
usuarios = {}

def guardar_datos_usuarios(datos):
    try:
        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo)
    except Exception as e:
        print("Error al guardar datos de usuarios:", e)

def cargar_datos_usuarios():
    try:
        with open("usuarios.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error al cargar datos de usuarios:", e)
        return {}



class Zembra(App):
    def build(self,):
        self.title = "Zembra"
        self.orientation = "vertical"
        layout = BoxLayout(orientation='vertical')
##INICIO PANTALLA
        self.layout = BoxLayout(orientation="vertical", spacing=40, padding=60)

        self.label = Label(text="¡Bienvenido a Zembra!")
        self.layout.add_widget(self.label)

        self.username_input = TextInput(hint_text="Usuario")
        self.layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Contraseña", password=True)
        self.layout.add_widget(self.password_input)

        self.registrar_btn = Button(text="Registrar", on_press=self.registrar)
        self.layout.add_widget(self.registrar_btn)

        self.iniciar_sesion_btn = Button(text="Iniciar Sesion", on_press=self.iniciar_sesion)
        self.layout.add_widget(self.iniciar_sesion_btn)

        return self.layout


##INICIO REGISTRO
    def registrar(self, instance):
        try:
            nombre_usuario = self.username_input.text
            contrasena = self.password_input.text

            if nombre_usuario in usuarios:
                self.label.text = "El nombre de usuario ya está registrado. Por favor, intenta con otro."
            else:
                usuarios[nombre_usuario] = contrasena
                guardar_datos_usuarios(usuarios)
                self.label.text = "¡Registro exitoso! Ahora puedes iniciar sesión."

        except Exception as e:
            self.label.text = "Ocurrió un error al registrar el usuario. Por favor, intenta nuevamente."
            print("Error al registrar usuario:", e)

    def iniciar_sesion(self, instance):
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

    def mostrar_pantalla_interactiva(self, *args):
        self.layout.clear_widgets()

        self.label.text = "¿En qué podemos ayudarte?"
        self.layout.add_widget(self.label)

        self.btn_scanner = Button(text="Escanea tu computador", on_press=partial(self.scanner))
        self.layout.add_widget(self.btn_scanner)

        self.btn_selector = Button(text="Selector de juego", on_press=partial(self.selector))
        self.layout.add_widget(self.btn_selector)

        self.btn_tres = Button(text="Consultar con Administración", on_press=partial(self.tres))
        self.layout.add_widget(self.btn_tres)

        self.btn_cerrar_aplicacion = Button(text="Cerrar Zembra", on_press=partial(self.cerrar_aplicacion))
        self.layout.add_widget(self.btn_cerrar_aplicacion)


    def scanner(self, *args):
        self.layout.clear_widgets()
        self.display_information("Información del Sistema: ", align="center", font_size=20, bold=True)
        self.obtener_informacion_sistema()
        self.display_information("\nInformación de la CPU: ", font_size=20, bold=True)
        self.obtener_informacion_cpu()
        self.display_information("\nInformación de la Memoria: ", font_size=20, bold=True)
        self.obtener_informacion_memoria()
        self.display_information("\nInformación Tarjeta Grafica: \n", font_size=20, bold=True)
        self.obtener_informacion_tarjeta_grafica()

        self.btn_volver = Button(text="Volver", on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)

    def obtener_informacion_sistema(self):
        sistema_operativo = platform.system()
        version_sistema = platform.version()
        arquitectura_sistema = platform.architecture()

        info_text = f"Versión del Sistema:{sistema_operativo},{version_sistema}\n" \
                    f"Arquitectura del Sistema: {arquitectura_sistema}"
        self.display_information(info_text)

    def obtener_informacion_cpu(self):
        cpu_info = platform.processor()
        num_cores = psutil.cpu_count(logical=False)
        num_threads = psutil.cpu_count(logical=True)

        info_text = f"Procesador: {cpu_info}\n" \
                    f"Número de Cores: {num_cores}\n" \
                    f"Número de Hilos: {num_threads}\n"
        self.display_information(info_text)

    def obtener_informacion_memoria(self):
        memoria_total = psutil.virtual_memory().total / (1024 ** 3)
        memoria_disponible = psutil.virtual_memory().available / (1024 ** 3)

        info_text = f"Memoria Total: {memoria_total:.2f} GB\n" \
                    f"Memoria Disponible: {memoria_disponible:.2f} GB"
        self.display_information(info_text)

    def obtener_informacion_tarjeta_grafica(self):
        sistema_operativo = platform.system()

        if sistema_operativo == "Windows":
            try:
                resultado = subprocess.check_output("wmic path win32_videocontroller get caption,driverversion", shell=True, text=True)
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
    
    def display_information(self, text, align="center", font_size=16, bold=False):
        label = Label(text=text, font_size=font_size, halign=align, bold=bold)
        self.layout.add_widget(label)


    def mostrar_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()


##A DEFINIR
    def tres(self,intance,*args):
        self.layout.clear_widgets()
        image = Image(source='ofi/ashe.jpeg', size_hint=( 1, 10))
        self.layout.add_widget(image)
        self.btn_volver = Button(text="Volver", on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)

##SELECTOR GAME
    def selector(self, instance):
        selected_game = instance.text
        self.layout.clear_widgets()
    
        self.game_label = Label(text="Juego seleccionado: " + selected_game)
        self.layout.add_widget(self.game_label)
    
        self.layout.add_widget(Label(text="Especificaciones mínimas:"))
    
        if selected_game in self.game_spinner.values:
            specifications = self.game_spinner.values[selected_game]
            for spec in specifications:
                self.layout.add_widget(Label(text=spec))
        else:
            self.layout.add_widget(Label(text="Seleccione un juego válido."))
    
        self.game_spinner = Spinner(
            text="Juegos",
            values={
                "League of legend": ["Core i3-530", "A6-3650", "GeForce 9600GT", "HD 6570", "RAM: 2 GB"],
                "Valorant": ["Intel Core 2 Duo E8400", "AMD Athlon 200GE", "Intel HD 4000", "AMD Radeon R5 200", "RAM: 4 GB"],
                "FIFA 24": ["Intel Core i5-6600K 3.50GHz", "AMD Ryzen 5 1600 3.2 GHZ", "NVIDIA GeForce GTX 1050 Ti 4GB", "AMD Radeon RX 570 4GB", "RAM: 8 GB"],
                "Call of Duty": ["Intel Core i5-6600 ", "AMD Ryzen 5 1400", "NVIDIA GeForce GTX 960", "GTX 1650", "AMD Radeon RX 470", "RAM: 8 GB"],
                "Counter Strike": ["Intel® Core™ 2 Duo E6600 ", "AMD Phenom™ X3 8750", "most be 256 MB", "RAM: 2GB"],
                "Minecraft": ["Intel Pentium D", "AMD Athlon 64", "Nvidia GeForce 9600 GT", "AMD Radeon HD 2400", "RAM: 2GB"],
                "GTA V": ["Intel Core 2 Quad CPU Q6600", "AMD Phenom 9850 Quad-Core", "NVIDIA 9800 GT 1GB", "AMD HD 4870 1GB", "RAM: 4GB"],
                "Fornite": ["Core i3-3225", "Intel HD 4000", "AMD Radeon Vega 8", "RAM: 8GB"],
            },
            on_text=self.selector
        )
        self.layout.add_widget(self.game_spinner)
    
        self.btn_volver = Button(text="Volver", on_press=self.mostrar_pantalla_interactiva)
        self.layout.add_widget(self.btn_volver)






##CIERRE APP
    def cerrar_aplicacion(self,intance,*args):
        self.stop()


##Fin
if __name__ == "__main__":
    try:
        usuarios = cargar_datos_usuarios()
        Zembra().run()
    except Exception as e:
        print("Error al ejecutar la aplicación:", e)
