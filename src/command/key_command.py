import pyautogui



occurrences = (['maximizar tela', 'maximizar', 'maximiza', 'maximize', 'maximizar tela',
                'minimizar tela', 'minimizar', 'minimiza', 'minimize', 'minimizar tela',
                'fechar tela', 'fechar', 'fecha', 'feche', 'fechar a tela',
                'aumentar tela', 'aumente a tela', 'aumente tela',
                'windows', 'sair','mudo', 'ativar mudo', 'desativar o volume', 
                'desativar o som', 'desativar o mudo',  'reativar o volume', 'reativar o som'
                'aumentar volume', 'aumentar o volume', 'aumentar o som','aumentar  som',
                'reduzir volume', 'reduzir o volume', 'reduzir o som', 'reduzir  som',
                'diminuir volume', 'diminuir o volume', 'diminuir o som', 'diminuir som'
                "pausar video", "pausar filme", "pausar vídeo", 'pausar o video', 'pausar o filme',
                "continuar video", "continuar filme", "continuar vídeo", 'continuar o video', 'continuar o filme',
                ])


def screnn_is_maximized():
    # Obter as dimensões da tela
    screen_width, screen_height = pyautogui.size()

    # Obter as dimensões da janela atual
    window = pyautogui.getActiveWindow()
    window_width, window_height = window.size

    # Verificar se a janela está maximizada
    return (window_width, window_height) == (screen_width, screen_height)


def router_key_command(world):

    if 'aumente' in world or 'aumentar' in world:
        pyautogui.hotkey('win', 'up')

    if 'maximize' in world or 'maximizar' in world:
        pyautogui.hotkey('f11')
        return f' Tela maximizada'

    if 'minimize' in world or 'minimizar' in world:
        if screnn_is_maximized():
            pyautogui.hotkey('f11')
        else:
            pyautogui.hotkey('win', 'down')
        return f' Tela minimizada'

    if 'fechar a tela' in world or 'fechar' in world or 'sair' in world:
        pyautogui.hotkey('alt', 'f4')
        return f' Tela fechada'

    if 'windows' in world:
        pyautogui.hotkey('win')
        return f' Windows aberto'
    
    if 'mudo' in world or 'ativar mudo' in world or 'desativar o mudo' in world:
        pyautogui.hotkey('volumemute')
        return f' Mudo ativado'

    
    if 'aumentar volume' in world or 'aumentar o volume' in world or 'aumentar o som' in world:
        if 'todo' in world or 'tudo' in world or 'total' in world or 'totalmente' in world or 'completamente' in world or 'inteiramente' in world or 'inteiro' in world or 'maximo' in world:
            for i in range(100):
                pyautogui.press('volumeup')
            return f' Volume aumentado no máximo'
        for i in range(10):
            pyautogui.press('volumeup')
        return f' Volume aumentado'
        
    if 'reduzir volume' in world or 'reduzir o volume' in world or 'reduzir o som' in world or 'diminuir volume' in world or 'diminuir o volume' in world or 'diminuir o som' in world:
        for i in range(10):
            pyautogui.hotkey('volumedown')
        return f' Volume reduzido'

    if 'pausar' in world or 'parar' in world:
        pyautogui.hotkey('space')
        return f' Video pausado'
    

def if_its_a_key_command(message):
    message = message.lower()
    query = message
    for term in occurrences:
        if term in message:
            if query is not None:
                return router_key_command(query)
    return None
