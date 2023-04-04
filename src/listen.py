import speech_recognition as sr

# Cria um reconhecedor de fala
r = sr.Recognizer()

# Define o modelo acústico e o modelo de linguagem para a língua portuguesa
acoustic_model = 'pt-br/acoustic_model'
language_model = 'pt-br/language_model.lm.bin'

# Define o arquivo de dicionário para a língua portuguesa
dictionary = 'pt-br/pronounciation.dict'

# Define o microfone como fonte de áudio
with sr.Microphone() as source:
    # Ajusta o nível de ruído do microfone
    r.adjust_for_ambient_noise(source)
    # Aguarda o usuário falar
    print('Fale alguma coisa...')
    audio = r.listen(source)
    print('Processando...')

# Realiza o reconhecimento de fala offline em português
try:
    text = r.recognize_sphinx(audio, language_model=language_model, 
                              acoustic_model=acoustic_model, 
                              dictionary=dictionary)
    print(f'Sua fala foi: {text}')
except sr.UnknownValueError:
    print('Não foi possível entender o que você disse.')
except sr.RequestError as e:
    print(f'Não foi possível conectar-se ao serviço de reconhecimento de fala: {e}')
