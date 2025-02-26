from customtkinter import *
from tkinter import Toplevel
from PIL import Image
import os

def registrar_usuario():
    # Obtén los valores ingresados por el usuario
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    nacimiento = entry_nacimiento.get()
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    # Puedes agregar lógica para el registro en tu base de datos o imprimir los valores
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    print("Año de Nacimiento:", nacimiento)
    print("Nombre de Usuario:", usuario)
    print("Contraseña:", contraseña)

def mostrar_ventana_registro():
    # Limpia el contenido del marco y muestra los campos de registro
    limpiar_frame()

    CTkLabel(master=frame, text="Nombre:",text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5), padx=(25, 0))
    entry_nombre_registro = CTkEntry(master=frame)
    entry_nombre_registro.pack()

    CTkLabel(master=frame, text="Apellido:",text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5), padx=(25, 0))
    entry_apellido_registro = CTkEntry(master=frame)
    entry_apellido_registro.pack()

    CTkLabel(master=frame, text="Año de Nacimiento:",text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5), padx=(25, 0))
    entry_nacimiento_registro = CTkEntry(master=frame)
    entry_nacimiento_registro.pack()

    CTkLabel(master=frame, text="Nombre de Usuario:",text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5), padx=(25, 0))
    entry_usuario_registro = CTkEntry(master=frame)
    entry_usuario_registro.pack()

    CTkLabel(master=frame, text="Contraseña:",text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5), padx=(25, 0))
    entry_contraseña_registro = CTkEntry(master=frame, show="*")
    entry_contraseña_registro.pack()

    # Botón para registrar usuario en el marco actual
    CTkButton(master=frame, text="Registrar", command=lambda: registrar_usuario_registro(entry_nombre_registro.get(), entry_apellido_registro.get(), entry_nacimiento_registro.get(), entry_usuario_registro.get(), entry_contraseña_registro.get())).pack(pady=(25, 0), padx=(0, 0))

    # Botón para volver a la pantalla de inicio
    CTkButton(master=frame, text="Volver", command=mostrar_inicio_sesion).pack()

def limpiar_frame():
    # Limpia el contenido del marco
    for widget in frame.winfo_children():
        widget.destroy()

# Función para el registro de usuario en el marco actual
def registrar_usuario_registro(nombre, apellido, nacimiento, usuario, contraseña):
    # Puedes agregar lógica para el registro en tu base de datos o imprimir los valores
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    print("Año de Nacimiento:", nacimiento)
    print("Nombre de Usuario:", usuario)
    print("Contraseña:", contraseña)

def mostrar_inicio_sesion():
    # Limpia el contenido del marco y muestra los elementos de inicio de sesión
    limpiar_frame()

    CTkLabel(master=frame, text="Bienvenido a Zembra", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Inicia sesión en tu cuenta", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000").pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*").pack(anchor="w", padx=(25, 0))

    # Botón para mostrar el formulario de registro en el marco actual
    CTkButton(master=frame, text="Registrate", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=mostrar_ventana_registro).pack()

    CTkButton(master=frame, text="Continuar Con Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=google_icon).pack(anchor="w", pady=(15, 0), padx=(25, 0))

# Obtén la ruta completa del directorio actual
directorio = os.path.dirname(os.path.abspath(__file__))

# Construye las rutas completas de las imágenes
side_img_path = os.path.join(directorio, "side-img.png")
email_icon_path = os.path.join(directorio, "email-icon.png")
password_icon_path = os.path.join(directorio, "password-icon.png")
google_icon_path = os.path.join(directorio, "google-icon.png")

app = CTk()
app.geometry("960x540")
app.resizable(0, 0)

# Abre las imágenes con Pillow
side_img_data = Image.open(side_img_path)
email_icon_data = Image.open(email_icon_path)
password_icon_data = Image.open(password_icon_path)
google_icon_data = Image.open(google_icon_path)

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

mostrar_inicio_sesion()

app.mainloop()
