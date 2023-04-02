
alfabeto = {
    "a": "a",
    "bê": "b",
    "cê": "c",
    "dê": "d",
    "ê": "e",
    "é": "é",
    "efe": "f",
    "gê": "g",
    "agá": "h",
    "i": "i",
    "jota": "j",
    "cá": "k",
    "ele": "l",
    "eme": "m",
    "ene": "n",
    "ó": "ó",
    "pê": "p",
    "quê": "q",
    "érre": "r",
    "esse": "s",
    "tê": "t",
    "u": "u",
    "vê": "v",
    "dáblio": "w",
    "xis": "x",
    "ípsilon": "y",
    "zê": "z"
}


def letter_as_pronounced(nome):
    return alfabeto.get(nome.lower(), None)


if __name__ == '__main__':
    print(letter_as_pronounced('a'))
    print(letter_as_pronounced('bê'))
    print(letter_as_pronounced('cê'))