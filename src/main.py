

import re
import os
import sys
import vosk
import json
import pyaudio
import speech_recognition as sr
from text_to_speech import speak
from unidecode import unidecode
from fuzzywuzzy import fuzz


# obter o cominho do arquivo
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from model import bot
from model import user
import router
from debug import log
from tools import clear_console
from config import BOT_NAME



audio = pyaudio.PyAudio()
model_path = f"{parent_dir}/model/vosk-model-pt/"
model = vosk.Model(model_path)
audio_device_index = 0  # Pode ser necessário ajustar
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True, frames_per_buffer=512,
                    input_device_index=audio_device_index)
recognizer = vosk.KaldiRecognizer(model, 16000)


def bot_command(text):
    print(text)
    text_token = text.split(' ')
    text = text.lower().replace('  ', ' ')
    similarity = fuzz.ratio(text_token[0], BOT_NAME.lower())
    if similarity > 60:  # ajuste o limiar de similaridade conforme necessário
        return text.replace(BOT_NAME.lower(), '')
    return None


def response(id_user, text, name_param):
    lila, status = router.process(id_user, text, name_param)
    lila = str(lila)
    # historic.historic_process(id_user, lila)
    response_ia = re.sub(r'[\(\)==.,]', ' ', lila)
    response_ia = re.sub(r'\s+', ' ', response_ia).strip()
    return response_ia, status


def voice_interaction_vosk(id_user, name_param):
    try:
        data = stream.read(512)
        print('Processando...')
        if len(data) == 0:
            pass
        # Reconhece o áudio
        if recognizer.AcceptWaveform(data):
            # Obtém o texto reconhecido
            result = json.loads(recognizer.Result())
            text = result["text"]
            return text
        return

    except Exception as error:
        log(error, f'{parent_dir}/logs/log.log')
        print('[ERRO]\n ', error, '\n')
        speak('Houve um erro. Por favor, tente novamente.')
        pass


def voice_interaction_google(rec, id_user, name_param):
    try:
        with sr.Microphone() as mic:
            rec.adjust_for_ambient_noise(mic, duration=0.2)
            audio = rec.listen(mic)
            print('Processando...')
            text = rec.recognize_vosk(audio, language='pt-BR')
            return text
    except sr.UnknownValueError:
        print('Não entendi o que você disse.')
        pass
    except sr.RequestError as e:
        print('Erro ao conectar ao Google Speech Recognition; {0}'.format(e))
        pass
    except Exception as error:
        log(error, f'{parent_dir}/logs/log.log')
        speak('Houve um erro. Por favor, tente novamente.')
        print('[ERRO]\n ', error, '\n')
        pass


def text_interaction(id_user, name_param):
    text = input('você:  ')
    if text == '':
        return
    return text


def message_process(id_user, name_param, user_input):
    clear_console()
    print('você:  ', user_input)
    user_input_if_is_command = bot_command(user_input)
    if user_input_if_is_command:
        assitant_response = response(
            id_user, user_input_if_is_command, name_param)
        speak(assitant_response)
        print('Lila:  ', assitant_response)
        return
    return


def main():
    print("Para ativar Lila, diga: 'Ok Lila'")
    speak('Olá, para interagir, diga: Ok Lila')
    rec = sr.Recognizer()
    id_user = "local"
    name_param = 'Amigo'
    while True:
        TEXT_MODE = os.environ.get('TEXT_MODE')
        LISTEN_ENGINE = os.environ.get('LISTEN_ENGINE')
        user_input = None
        try:
            if TEXT_MODE == 'False':
                if LISTEN_ENGINE == 'vosk':
                    user_input = voice_interaction_vosk(id_user, name_param)
                if LISTEN_ENGINE == 'google':
                    user_input = voice_interaction_google(
                        rec, id_user, name_param)
            else:
                user_input = text_interaction(id_user, name_param)
            message_process(id_user, name_param, user_input)

        except Exception as error:
            log(error, f'{parent_dir}/logs/log.log')
            speak('Houve um erro. Por favor, tente novamente.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='voice')
    parser.add_argument('--listenEngine', type=str, default='vosk')
    args = parser.parse_args()
    clear_console()
    print(f"Modo: {args.mode}")
    print(f"Engine de reconhecimento: {args.listenEngine}")
    try:
        if args.mode == 'text':
            os.environ['TEXT_MODE'] = 'True'
        if args.mode == 'voice':
            os.environ['TEXT_MODE'] = 'False'
        if args.listenEngine == 'google':
            os.environ['LISTEN_ENGINE'] = 'google'
        if args.listenEngine == 'vosk':
            os.environ['LISTEN_ENGINE'] = 'vosk'
        main()
    except Exception as error:
        log(error, f'{parent_dir}/logs/log.log')
        speak('Houve um erro. Por favor, tente novamente.')

