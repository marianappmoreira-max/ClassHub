import sqlite3


BANCO = "classhub.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_usuario(nome, usuario, senha, tipo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nome, usuario, senha, tipo)
        VALUES (?, ?, ?, ?)
    """, (nome, usuario, senha, tipo))

    conexao.commit()
    conexao.close()


def buscar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()

    conexao.close()

    return resultado


def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, usuario
        FROM usuarios
        WHERE tipo = 'aluno'
    """)

    resultado = cursor.fetchall()

    conexao.close()

    return resultado
