import pyautogui

occurrences = (['maximizar tela', 'maximizar', 'maximiza', 'maximize', 'maximizar tela',
                'minimizar tela', 'minimizar', 'minimiza', 'minimize', 'minimizar tela',
                'fechar tela', 'fechar', 'fecha', 'feche', 'fechar a tela',
                'aumentar tela', 'aumente a tela', 'aumente tela',
                'windows', 'sair'
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


def if_its_a_key_command(message):
    message = message.lower()
    query = message
    for term in occurrences:
        if term in message:
            if query is not None:
                return router_key_command(query)
    return None
