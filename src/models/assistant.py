import os
import re
import vosk
import json
import pygame
import pyaudio
import pyttsx3
import tempfile
import threading
import pyttsx3.voice
from enum import Enum
from typing import Any
from fuzzywuzzy import fuzz
import speech_recognition as sr
from google.cloud import texttospeech
from pydantic import BaseModel, validator

parent_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class Assistant(BaseModel):
    name: str = 'Assistant'
    interaction_mode: str = 'voice'
    voice_recognition_engineering: str = 'vosk'
    microphone: str = 0
    voice_reproduction_engineering: str = 'google'
    stream: Any = None
    rec: Any = None
    recognizer: Any = None
    voice_language: str = 'pt-BR'
    voice_name: str = 'pt-BR-Wavenet-A'
    sp_engine: Any = None
    client: Any = None
    command_to_activate: str = None
    command_to_activate_similarity: int = 60
    
    class Config:
        use_enum_values = True

    class InteractionModeEnum(str, Enum):
        voice = "voice"
        text = "text"

    class VoiceRecognitionEngineeringEnum(str, Enum):
        vosk = "vosk"
        google = "google"

    class VoiceReproductionEngineeringEnum(str, Enum):
        default = "google"
        google = "google_cloud"

    @validator("interaction_mode")
    def validate_interaction_mode(cls, value):
        if value != "voice":
            raise ValueError("The 'interaction_mode' option must be 'voice'")
        return value

    @validator("voice_recognition_engineering")
    def validate_recognition_engine(cls, value):
        if value != "vosk" and value != "google":
            raise ValueError(
                "The 'voice_recognition_engineering' option must be 'vosk' or 'google'")
        return value

    @validator("voice_reproduction_engineering")
    def validate_reproduction_engine(cls, value):
        if value != "google" and value != "google_cloud":
            raise ValueError(
                "The 'voice_reproduction_engineering' option must be 'google' or 'google_cloud'")
        return value

    @validator("voice_name")
    def validate_voice_name(cls, value):
        if value != "pt-BR-Wavenet-A" and  value != "pt-BR-Wavenet-B" and  value != "pt-BR-Wavenet-C":
            raise ValueError(
                "The 'voice_name' option must be 'pt-BR-Wavenet-A' or 'pt-BR-Wavenet-B' or 'pt-BR-Wavenet-C'")
        return value

    def initialize_voice_recognition_engine(self):
        if self.voice_recognition_engineering == 'vosk':
            audio = pyaudio.PyAudio()
            model_path = f"{parent_dir}/model/vosk-model-pt/"
            model = vosk.Model(model_path)
            audio_device_index = self.microphone  # Pode ser necessário ajustar
            self.stream = audio.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=16000,
                                     input=True, frames_per_buffer=512,
                                     input_device_index=audio_device_index)
            self.recognizer = vosk.KaldiRecognizer(model, 16000)

        elif self.voice_recognition_engineering == 'google':
            self.rec = sr.Recognizer()
            self.stream = None

    def voice_interaction(self):
        if self.voice_recognition_engineering == 'vosk':
            data = self.stream.read(512)
            print('Processando...')
            if len(data) == 0:
                pass
            # Reconhece o áudio
            if self.recognizer.AcceptWaveform(data):
                # Obtém o texto reconhecido
                result = json.loads(self.recognizer.Result())
                text = result["text"]
                print(text)
                return text
            return
        elif self.voice_recognition_engineering == 'google':
            try:
                with sr.Microphone(self.microphone) as mic:
                    self.rec.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.rec.listen(mic, timeout=5, phrase_time_limit=5, snowboy_configuration=None)
                    print('Processando...')
                    text = self.rec.recognize_google(audio, language='pt-BR')
                    return text
            except sr.UnknownValueError:
                print('Não entendi o que você disse.')
                pass

    def google_cloud_credentials(self, GOOGLE_APPLICATION_CREDENTIALS):
        if self.voice_reproduction_engineering == 'google_cloud':
            if GOOGLE_APPLICATION_CREDENTIALS is None:
                raise ValueError(
                    "The 'GOOGLE_APPLICATION_CREDENTIALS' environment variable must be set")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
            self.client = texttospeech.TextToSpeechClient()

    def initialize_voice_reproduction_engine(self):
        if self.voice_reproduction_engineering == 'google':
            self.sp_engine = pyttsx3.init()
            self.sp_engine.setProperty('rate', 150)
            self.sp_engine.setProperty('volume', 0.9)
            self.sp_engine.setProperty('voice', self.voice_name)
            self.sp_engine.setProperty('language', self.voice_language)
        if self.voice_reproduction_engineering == 'google_cloud':
            pass

    def speak(self, text_to_speak):
        if self.voice_reproduction_engineering == 'google':
            voices = self.sp_engine.getProperty('voices')
            self.sp_engine.setProperty('voice', voices[0].id)
            self.sp_engine.say(text_to_speak)
            self.sp_engine.runAndWait()
            self.sp_engine.stop()

        if self.voice_reproduction_engineering == 'google_cloud':
            synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.voice_language,
                name=self.voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            audio_reproduction(write_file(response))

    def its_a_assistant_command(self, user_text):
        if user_text is None:
            return None
        
        user_text = user_text.lower().replace('  ', ' ')
        text_token = user_text.split(' ')
        user_test_without_command = " ".join(text_token[1:])
        text_to_analize = " ".join(text_token[:1])
        text_to_activate = self.name
        
        if self.command_to_activate:
            text_to_activate = f'{self.command_to_activate} {self.name}'
            user_test_without_command = " ".join(text_token[2:])
            text_to_analize = " ".join(text_token[:2])
            
            
        similarity = fuzz.ratio(text_to_analize.lower(), text_to_activate.lower())
        if similarity >= self.command_to_activate_similarity:
            return user_test_without_command.strip()
        return None



def audio_reproduction(audio_file):
    pygame.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass
    pygame.quit()
    t = threading.Thread(target=delete_file, args=(audio_file,))
    t.start()


def delete_file(filename):
    os.remove(filename)

    
def write_file(audio_bitecode):
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        temp_file.write(audio_bitecode.audio_content)
        return temp_file.name
