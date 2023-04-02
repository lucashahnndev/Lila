import memory
from chatterbot_bot import response_to_user
from greeting import if_its_a_greeting


# config

# frases

def process(id_user, mensagem, name_param):
        global name
        name = name_param
        result = 0

        if_greeting = if_its_a_greeting(mensagem, name)
        if if_greeting is not None:
            result = 1
            return if_greeting

        memory_a = memory.do_not_know(id_user, mensagem)
        if memory_a is not None:
            result = 1
            return memory_a
        
        if result == 0:
            return response_to_user(mensagem)
