import re
import pyttsx3
import pyttsx3.voice
import sys
import os
import threading
from google.cloud import texttospeech
import time
import pygame

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
TEXT_MODE = os.environ.get('TEXT_MODE')

from debug import log
from config import BOT_NAME
    
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{os.path.dirname(parent_dir)}\\data\\Lia-5732d88a57a2.json'
audio_file = f'{os.path.dirname(parent_dir)}\data\cache\output.mp3'


def write_file(response):
    with open(audio_file, 'wb') as out:
        out.write(response.audio_content)
        out.close()
    return response
        

def speak_with_voice(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='pt-BR',
        name='pt-BR-Wavenet-C',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    audio_reproduction(write_file(response))

def audio_reproduction(audio_file):
    pygame.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass
    pygame.quit()
    
def speak(text):
    TEXT_MODE = os.environ.get('TEXT_MODE')
    try:
        if TEXT_MODE == 'False':
            print('Modo texto desativado')
            speak_with_voice(text)
        else:
            print('Modo texto ativado')
        print(f'{BOT_NAME}:  ', text)
    except Exception as error:
        log(error, 'logs/log.log')

if __name__ == "__main__":
    os.environ['TEXT_MODE'] = 'False'
    while True:
        user = input('Digite algo: ')
        speak(user)
