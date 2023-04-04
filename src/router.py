# import memory
# from chatterbot_bot import response_to_user
from greeting import if_its_a_greeting
from command import if_its_a_command_open_program, if_its_a_command_search, if_its_a_key_command, if_its_a_command_play_in_youtube
from text_to_speech import speak
import os


# obter o cominho do arquivo
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def process(id_user, mensagem, name_param):
    global name
    name = name_param
    result = 0
    if mensagem.lower() == 'sair do chat':
        speak('Até  mais.')
        exit()

    if mensagem.lower() == 'exibir logs':
        os.popen(f'start {parent_dir}\logs\log.log')
        return 'Exibindo logs.'

    if mensagem.lower() == 'desativar modo texto':
        os.environ['TEXT_MODE'] = 'False'
        return 'Modo texto desativado.'

    if mensagem.lower() == 'ativar modo texto':
        os.environ['TEXT_MODE'] = 'True'
        return 'Modo texto ativado.'

    if__key_command = if_its_a_key_command(mensagem)
    if if__key_command is not None:
        result = 1
        return if__key_command

    if__youtube = if_its_a_command_play_in_youtube(mensagem)
    if if__youtube is not None:
        result = 1
        return if__youtube

    if__search = if_its_a_command_search(mensagem)
    if if__search is not None:
        result = 1
        return if__search

    if__command = if_its_a_command_open_program(mensagem)
    if if__command is not None:
        result = 1
        return if__command

    if_greeting = if_its_a_greeting(mensagem, name)
    if if_greeting is not None:
        result = 1
        return if_greeting

    """ memory_a = memory.do_not_know(id_user, mensagem)
        if memory_a is not None:
            result = 1
            return memory_a """

    if result == 0:
        return 'Não entendi o que você quis dizer.'
        #return response_to_user(mensagem)
