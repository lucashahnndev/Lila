import re
from debug import log
import pyttsx3
import sys
import os
import threading


TEXT_MODE = os.environ.get('TEXT_MODE')

def clean_text(text):
    """
    Função que limpa o texto de caracteres especiais e substitui algumas abreviações.
    """
    # substitui o grau pelo texto "graus"
    text = text.replace("º", " graus ")

    # substitui aspas simples e duplas por nada
    text = text.replace("'", "")
    text = text.replace('"', '')

    # substitui abreviações por seus significados
    abbreviations = {"cm": "centímetros", "kg": "quilogramas", "mm": "milímetros",
                     "cm²": "centímetros quadrados", "m²": "metros quadrados", "km²": "quilômetros quadrados", "+": "mais", "-": "menos", "*": "vezes", "/": "dividido por","=":"igual a"}
    for abbreviation, meaning in abbreviations.items():
        text = text.replace(abbreviation, meaning)

    return text


def remove_special_chars(text):
    """
    Remove caracteres especiais que podem ser problemáticos para softwares de transcrição de voz.
    """
    cleaned_text = clean_text(text)
    return re.sub(r'[^\w\s]', '', cleaned_text)

def speak_with_voice(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.say(text)
        engine.runAndWait()
    finally:
        engine.stop()

  
def speak(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    TEXT_MODE = os.environ.get('TEXT_MODE')
    try:
        if TEXT_MODE == 'False':
            print('Modo texto desativado')
            thread_speak = threading.Thread(target=speak_with_voice, args=(text,))
            thread_speak.start()
        else:
            print('Modo texto ativado')
        print('Solhia:  ', text)
    except Exception as error:
        log(error, 'logs/log.log')
    
