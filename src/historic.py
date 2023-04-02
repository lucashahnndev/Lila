import pickle
from  os import path


def historic_process(id_telegram, mensagem_from_bot):
    historic = []
    file_name = f"historic/{id_telegram}.pkl"
    if path.exists(file_name):
        open_file = open(file_name, "rb")
        historic = pickle.load(open_file)
        open_file.close()
        last_item = historic[-1]
    else:
        last_item = ''

    historic.append(mensagem_from_bot)
    open_file = open(file_name, "wb")
    pickle.dump(historic, open_file)
    open_file.close()
    return last_item


def query(id_telegram):
    historic = []
    file_name = f"historic/{id_telegram}.pkl"
    if path.exists(file_name):
        open_file = open(file_name, "rb")
        historic = pickle.load(open_file)
        open_file.close()
        return historic[-1]
    else:
        return None
