import re
import os
import sys
import router
import historic
from debug import log
import speech_recognition as sr
from text_to_speech import speak
# import open_ai_conector


# obter o cominho do arquivo
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ir para parent_dir
sys.path.append(parent_dir)


def response(id_user, texto, name_param):
    bia = str(router.process(id_user, texto, name_param))
    historic.historic_process(id_user, bia)
    response_ia = re.sub(r'[\(\)==.,]', ' ', bia)
    response_ia = re.sub(r'\s+', ' ', response_ia).strip()
    return response_ia


os.system('cls' if os.name == 'nt' else 'clear')


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
                    #rec.adjust_for_ambient_noise(mic)
                    audio = rec.listen(mic)
                    texto = rec.recognize_google(audio, language='pt-BR')
                    print('você:  ', texto)
                    res = response(id_user, texto, name_param)
                    speak(res)
            else:
                texto = input('você:  ')
                if texto == '':
                    continue
                res = response(id_user, texto, name_param)
                speak(res)

        except sr.UnknownValueError:
            #speak('Não conssegui entender o que você disse. Por favor, repita.')
            pass
        except Exception as error:
            log(error, f'{parent_dir}/log.log')
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
            speak('Fale alguma coisa')
        main()
    except Exception as error:
        log(error, f'{parent_dir}/logs/log.log')
        speak('Houve um erro. Por favor, tente novamente.')
