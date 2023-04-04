import random
#import subprocess
import text_to_speech
import os
import threading
#import webbrowser
#from open_internet_service import open_internet_app
import pyautogui

occurrences = (['abrir', 'abre','abra', 'executar', 'executa','execute', 'rode', 'rodar', 'iniciar', 'inicia', 'inicie'])
aditional_occurrences = ['o',  'a']

confirmation = ([
    'abrindo',
    'iniciando',
    'executando',
    'rodando'
])

confirm = (['O app foi executado com sucesso.', "aberto com sucesso", "iniciado com sucesso",
           "executado com sucesso", "rodado com sucesso", "O app foi iniciado com sucesso.",  " foi executado com sucesso."])


def remove_aditional_terms(query, term, aditional_search_terms):
    query = query.replace('  ', ' ')
    query = query.replace(f'{term}', '_*_')
    for aditional_term in aditional_search_terms:
        if aditional_term in query:
            query = query.replace(f'{aditional_term} _*_', '_*_')
            query = query.replace(f'_*_ {aditional_term}', '_*_')
    return query.replace('_*_', '')

def open_program(program, program_=None):
    try:
        res = os.popen(f'start /b {program} || echo _*erro*_.').read()
        if "_*erro*_" in res:
            text_to_speech.speak(
                f'Desculpe não encontrei um programa chamado {program_}')
        return res
    except Exception as e:
        print("Erro\n   ", e)
        text_to_speech.speak(
                f'Desculpe não encontrei um programa chamado {program_}')

def open_internet_app(program, url, program_=None ):
    try:
        res = os.popen(f'start /b chrome -app={url} --start-fullscreen || echo _*erro*_.').read()
        pyautogui.sleep(5)

        # pressiona a tecla F11 para maximizar a janela
        pyautogui.hotkey('f11')

        if "_*erro*_" in res:
            text_to_speech.speak(
                f'Desculpe não encontrei um programa chamado {program_}')
        return res
    except Exception as e:
        print("Erro\n   ", e)
        text_to_speech.speak(
                f'Desculpe não encontrei um programa chamado {program_}') 


def run_program(program):
    program_ = program
    program = f'{program.strip()}'
    webbrowser_ = False
    url = ''
    if 'notas' in program or 'bloco de notas' in program:
        program = 'notepad'
        
    if 'netflix' in program:
        webbrowser_ = True
        url = 'https://www.netflix.com/br/'
        
    if 'youtube' in program:
        webbrowser_ = True
        url = 'https://www.youtube.com/'
    
    if 'star plus' in program:
        webbrowser_ = True
        url = 'https://www.starplus.com/pt-br'    
        
    if 'disney plus' in program:
        webbrowser_ = True
        url = 'https://www.disneyplus.com/pt-br'
    
    if 'prime video' in program:
        webbrowser_ = True
        url = 'https://www.primevideo.com/'
        
    if 'hbomax' in program or 'hbo' in program:
        webbrowser_ = True
        url = 'https://play.hbomax.com/'
    
    if webbrowser_ == False:
        open_program(program,program_=program_)
    else:
        open_internet_app(program, url )
    




def if_its_a_command_open_program(message):
    message = message.lower()
    query = message
    for term in occurrences:
        if term in message:
            query = remove_aditional_terms(query, term, aditional_occurrences)
            if query is not None:
                run_program_ = threading.Thread(
                    target=run_program, args=(query,))
                run_program_.start()
                return f'{random.choice(confirmation)} {query}'
    return None