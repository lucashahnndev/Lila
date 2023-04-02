import  re
import router
import historic
from debug import log
import speech_recognition as sr
from text_to_speech import speak

rec = sr.Recognizer()
id_user = 123
name_param = 'Amigo'


def response(id_user, texto, name_param):
    bia = str(router.process(id_user, texto, name_param))
    historic.historic_process(id_user, bia)
    response_ia = re.sub(r'[\(\)==.,]', ' ', bia)
    response_ia = re.sub(r'\s+', ' ', response_ia).strip()
    speak(response_ia)
    return response_ia
        
        
        
def main():
    while True:
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic)
                audio = rec.listen(mic)
                texto = rec.recognize_google(audio, language='pt-BR')
                print('você:  ', texto)
                response(id_user, texto, name_param)

        except sr.UnknownValueError:
            print('Solhia:   Não entendi')
            pass
        except Exception as error:
            log(error, 'logs/log.log')
            speak('Houve um erro. Por favor, tente novamente.')
            exit()


if __name__ == '__main__':
    speak('Fale alguma coisa')
    main()