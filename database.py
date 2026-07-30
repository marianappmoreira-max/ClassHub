import json


ARQUIVO_USUARIOS = "dados/usuarios.json"


def carregar_usuarios():
    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            usuarios,
            arquivo,
            indent=4,
            ensure_ascii=False
        )
