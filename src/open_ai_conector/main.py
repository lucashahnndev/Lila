import openai
from config import OPENAI_API_KEY

openai.organization = "org-RzXfrXb5V3VEZzCqNOUBka9s"
openai.api_key = OPENAI_API_KEY
#list = openai.Model.list()
#este codigo é um modulo de conexção com a api do open ai
#https://beta.openai.com/docs/api-reference/create-completion
#usa o modelo gpt-3.5-turbo
#usado para criar uma conversa
#a função deve receber uma pergunta e retornar uma resposta

""" def response_to_user(mensagem):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": mensagem}]
    )
    return completion.choices[0].text
 """

completion = openai.Completion()

start_chat_log = '''Human: De agora em diante você será meu assistente virtual. seu nome será Solhia.
AI: Ok, de agora em diante meu nome é Solhia. como posso te ajudar?
'''
def response_to_user(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer
