import random
import os
import pyautogui
from config import GOOGLE_CLOUD_API_KEY
from googleapiclient.discovery import build


search_terms = ['pesquisar no youtube ', 'pesquise no youtube', 'pesquisa no youtube',
                'tocar no youtube', 'toque no youtube', 'toca no youtube',
                'abre no youtube', 'abrir no youtube', 'abra no youtube',
                'reproduzir no youtube', 'reproduza no youtube',
                'rode no youtube', 'rodar no youtube', 'roda no youtube',
                "no youtube", "youtube"
                ]

aditional_search_terms = ['sobre ', 'sobre o ', 'sobre a ', 'por ', 'faça uma ', 'realize uma ', 'de ',
                          'video de ', 'video do ', 'video da ',
                          'desenho do ', 'desenho da', 'desenho de ', 
                          'filme do', 'filme da', 'filme de ',
                          'musica da ', 'musica de ', 'musica do ', 
                          'filme de ', 'filme da ', 'filme do ']

confirmation = ([
    "reprodusindo a primeira opção de",
    "abrindo a primeira opção de",
    "tocando a primeira opção de",
    "rodando a primeira opção de",
    "reproduzindo a primeira ocorrencia de",
    "abrindo a primeira ocorrencia de",
    "tocando a primeira ocorrencia de",
    "rodando a primeira ocorrencia de",
    ])
ok = (["ok", "certo", "entendido", "sim", "claro"])

def play_in_youtube(query):
    # constrói o serviço da API de pesquisa do YouTube
    youtube_service = build('youtube', 'v3', developerKey=GOOGLE_CLOUD_API_KEY)
    bronser = 'chrome '
    # envia uma solicitação de pesquisa para a API do YouTube e obtém o ID do vídeo do primeiro resultado
    search_response = youtube_service.search().list(
        q=query.replace(' ', '+'),
        part='id,snippet',
        type='video',
        videoDefinition='high',
        maxResults=1
    ).execute()
    # obtém o ID do vídeo do primeiro resultado da pesquisa
    video_id = search_response['items'][0]['id']['videoId']
    
    # define a URL do vídeo
    url = f"-app=https://www.youtube.com/watch?v={video_id}"
    if bronser == 'microsoft-edge:':
        url = f"https://www.youtube.com/watch?v={video_id}"
    print(url)
    os.popen(f"start {bronser}{url}")
    pyautogui.sleep(5)
    #preciona a tecla f para maximizar a janela
    pyautogui.hotkey('f')
    # pressiona a tecla F11 para maximizar a janela
    pyautogui.hotkey('f11')

    return f'{random.choice(ok)}, {random.choice(confirmation)} {query} no youtube'


def remove_aditional_terms(query, term, aditional_search_terms):
    query = query.replace('  ', ' ')
    query = query.replace(f'{term}', '_*_')
    for aditional_term in aditional_search_terms:
        if aditional_term in query:
            query = query.replace(f'{aditional_term} _*_', '_*_')
            query = query.replace(f'_*_ {aditional_term}', '_*_')
    return query.replace('_*_', '')


def if_its_a_command_play_in_youtube(message):  
    message = message.lower()
    query = message
    for term in search_terms:
        if term in message:
            query = remove_aditional_terms(query, term, aditional_search_terms)
            if query is not None:
                return play_in_youtube(query)
    return None


"""
from googleapiclient.discovery import build
import webbrowser

# define a palavra-chave de busca
search_query = "python tutorial"

# constrói o serviço da API de pesquisa do YouTube
youtube_service = build('youtube', 'v3', developerKey='sua-chave-de-API')

# envia uma solicitação de pesquisa para a API do YouTube e obtém o ID do vídeo do primeiro resultado
search_response = youtube_service.search().list(
    q=search_query,
    part='id,snippet',
    type='video',
    videoDefinition='high',
    maxResults=1
).execute()

# obtém o ID do vídeo do primeiro resultado da pesquisa
video_id = search_response['items'][0]['id']['videoId']

# define a URL do vídeo
video_url = f'https://www.youtube.com/watch?v={video_id}'

# abre a URL do vídeo no navegador padrão em tela cheia e com autoplay
webbrowser.open(video_url, new=0, autoraise=True)

"""
