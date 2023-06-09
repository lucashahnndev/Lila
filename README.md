# Lila

Lila é uma assistente pessoal baseada em Python que utiliza reconhecimento de voz e gestos para interação. O projeto foi desenvolvido para o sistema operacional Windows e possui funcionalidades como meteorologia, curiosidades, abertura de programas e streams, agenda, tarefas, entre outros.

## Arquitetura de diretórios

A Lila segue a seguinte estrutura de diretórios:

```
Lila/
├── audio/                  # Arquivos de áudio para a interação com a assistente
│   ├── greeting.wav
│   ├── command_received.wav
│   ├── recognition_error.wav
│   └── ...
├── corpus/                   # corpus de treinamento
|   ├── portuguese/          # Corpus em português
|   |   └── ...
|   └── ...
├── data/                   # Dados necessários para o funcionamento da assistente
|   ├── config.json         # Configurações da assistente
│   ├── agenda.txt
│   ├── curiosities.json
│   └── ...
├── model/                  # Modelos de reconhecimento de voz e gestos
│   ├── gesture_detection.pkl
│   └── speech_recognition.pkl
├── src/                    # Código-fonte da Lila
│   ├── __init__.py
│   ├── agenda.py
│   ├── audio.py
│   ├── commands.py
│   ├── curiosities.py
│   ├── gestures.py
│   ├── main.py
│   ├── recognizer.py
│   ├── speech.py
│   └── ...
├── LICENSE
├── README.md
└── requirements.txt
```

## Instalação

1. Clone o repositório: `git clonehttps://github.com/lucashahnndev/Lila.git`
2. Instale as dependências: `pip install -r requirements.txt`

## Utilização

1. Abra o terminal na pasta do projeto
2. Execute o arquivo `main.py`: `python main.py`
3. Siga as instruções de voz e gestos para interagir com a Lila

## Funcionalidades

A Lila possui diversas funcionalidades, incluindo:

- Meteorologia: Obtém informações sobre o tempo em uma determinada cidade
- Curiosidades: Fornece curiosidades aleatórias sobre vários tópicos
- Abrir programas: Abre programas instalados no computador
- Abrir streams: Abre streams e possibilita controlá-los por meio de comandos de voz
- Agenda: Armazena eventos e lembretes
- Tarefas: Armazena tarefas e possibilita sua conclusão

## Contribuição

Você pode contribuir para o desenvolvimento da Lila reportando bugs, sugerindo novas funcionalidades ou enviando pull requests.

## Licença

Este projeto está sob a Licença BSD 3-cláusula "New". Consulte o arquivo `LICENSE` para obter mais informações.
