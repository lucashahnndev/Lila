import re
import os
import sys
import router
import historic
import time
from debug import log
import speech_recognition as sr
from text_to_speech import speak
from unidecode import unidecode
from config import BOT_NAME
# import open_ai_conector


# obter o cominho do arquivo
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ir para parent_dir
sys.path.append(parent_dir)


def response(id_user, text, name_param):
    lila = str(router.process(id_user, text, name_param))
    historic.historic_process(id_user, lila)
    response_ia = re.sub(r'[\(\)==.,]', ' ', lila)
    response_ia = re.sub(r'\s+', ' ', response_ia).strip()
    return response_ia


os.system('cls' if os.name == 'nt' else 'clear')


def bot_activation(text):
    text = text.lower().replace('  ',' ')
    comand_actvation = f'ok {BOT_NAME}'
    if comand_actvation.lower() in text:
        return text.replace(comand_actvation.lower(), '')
    return None
   

def main():
    id_user = "local"
    name_param = 'Amigo'
    rec = sr.Recognizer()
    id_user = 123
    name_param = 'Amigo'
    while True:
        TEXT_MODE = os.environ.get('TEXT_MODE')
        try:
            if TEXT_MODE == 'False':
                with sr.Microphone() as mic:
                    rec.adjust_for_ambient_noise(mic)
                    print("Diga alguma coisa: ")
                    audio = rec.listen(mic)
                    print('Processando...')
                    text = rec.recognize_google(audio, language='pt-BR')
                    if bot_activation(text):
                        print('você:  ', text)
                        res = response(id_user, text, name_param)
                        speak(res)
                    print('você:  ', text)
                    continue
            else:
                text = input('você:  ')
                if text == '':
                    continue
                res = response(id_user, text, name_param)
                speak(res)

        except sr.UnknownValueError:
            pass
        except Exception as error:
            log(error, f'{parent_dir}/logs/log.log')
            speak('Houve um erro. Por favor, tente novamente.')
            exit()


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2 :
            if sys.argv[1] == 'text':
                os.environ['TEXT_MODE'] = 'True'
                print('Modo texto ativado')
        else:
            os.environ['TEXT_MODE'] = 'False'
            print('Modo texto desativado')
            #speak('Fale alguma coisa')
        speak("Olá, meu nome é Lila, e sou a sua assistente virtual. Como posso ajudar?")
        main()
    except Exception as error:
        log(error, f'{parent_dir}/logs/log.log')
        speak('Houve um erro. Por favor, tente novamente.')
