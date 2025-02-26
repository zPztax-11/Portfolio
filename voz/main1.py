import speech_recognition as sr
import pyttsx3
from gtts import gTTS
# Inicia el reconocimiento de voz
recognizer = sr.Recognizer()

def escuchar():
    with sr.Microphone() as source:
        print("Di algo:")
        audio = recognizer.listen(source)

        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            print(f"Escuchado: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError:
            print("Error en la conexión con el servicio de reconocimiento de voz")

def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

if __name__ == "__main__":
    texto = escuchar()
    if texto:
        respuesta = "Has dicho: " + texto
        hablar(respuesta)
