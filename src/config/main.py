import json
import sys
import os
#obter o cominho do arquivo
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#ir para parent_dir
sys.path.append(parent_dir)


file_config = open(f'{parent_dir}\\data\\config.json', 'r')
config = json.load(file_config)

BOT_NAME = config['chatterbot']['nameBot']

OPENAI_API_KEY = config['openai']['token']

