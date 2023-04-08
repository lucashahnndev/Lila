from models.assistant import Assistant
import sys
import os
import router
from tools import clear_console
import random

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# create an instance of the Assistant class
Lila = Assistant(voice_recognition_engineering='google',
                 voice_reproduction_engineering='google_cloud',
                 voice_language='pt-BR',
                 voice_name='pt-BR-Wavenet-C',
                 name='Lila',
                 )
Lila.google_cloud_credentials(f'{parent_dir}\\data\\Lia-5732d88a57a2.json')

# initialize the voice recognition engine
Lila.initialize_voice_recognition_engine()
Lila.initialize_voice_reproduction_engine()


acitivation_comfirm = ['Sim, como posso ajudar?', 'Sim, o que deseja?', 'Sim, o que posso fazer por você?', 'Olá, como posso ajudar?', 'Olá, o que deseja?',
                       'Olá, o que posso fazer por você?', 'Olá, como posso ser útil?', 'Olá, como posso ajudar?', 'Olá, o que deseja?', 'Olá, o que posso fazer por você?', 'Olá, como posso ser útil?']

clear_console()
skip_activation_command = False
while True:
    transcription = Lila.voice_interaction()
    clear_console()
    print('Transcription:', transcription)
    user_input_without_command = transcription
    if skip_activation_command == False:
        user_input_without_command = Lila.its_a_assistant_command(
            transcription)
        if user_input_without_command == '':
            skip_activation_command = True
            Lila.speak(random.choice(acitivation_comfirm))
            continue
    else:
        skip_activation_command = False

    print('User input without command:', user_input_without_command)
    if transcription == None or user_input_without_command == None:
        continue
    res, _ = router.process(1, user_input_without_command, 'senhor')
    print('Lila response:', res)
    Lila.speak(res)
