import sqlite3
import hashlib


BANCO = "classhub.db"


def proteger_senha(senha):
    return hashlib.sha256(
        senha.encode()
    ).hexdigest()



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


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            observacao TEXT,
            FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
        )
    """)


    conexao.commit()
    conexao.close()



# ======================
# USUÁRIOS
# ======================


def adicionar_usuario(nome, usuario, senha, tipo):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        INSERT INTO usuarios
        (nome, usuario, senha, tipo)
        VALUES (?, ?, ?, ?)
    """, (
        nome,
        usuario,
        proteger_senha(senha),
        tipo
    ))


    conexao.commit()
    conexao.close()



def buscar_usuario(usuario):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT *
        FROM usuarios
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



def listar_alunos_com_id():

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT id, nome
        FROM usuarios
        WHERE tipo = 'aluno'
    """)


    resultado = cursor.fetchall()


    conexao.close()

    return resultado



# ======================
# AULAS
# ======================


def adicionar_aula(aluno_id, data, conteudo, observacao):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        INSERT INTO aulas
        (aluno_id, data, conteudo, observacao)
        VALUES (?, ?, ?, ?)
    """, (
        aluno_id,
        data,
        conteudo,
        observacao
    ))


    conexao.commit()
    conexao.close()



def listar_todas_aulas():

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT
            usuarios.nome,
            aulas.data,
            aulas.conteudo,
            aulas.observacao
        FROM aulas

        INNER JOIN usuarios
        ON aulas.aluno_id = usuarios.id

        ORDER BY aulas.id DESC
    """)


    resultado = cursor.fetchall()


    conexao.close()

    return resultado



def buscar_aulas_por_usuario(usuario):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT
            aulas.data,
            aulas.conteudo,
            aulas.observacao

        FROM aulas

        INNER JOIN usuarios
        ON aulas.aluno_id = usuarios.id

        WHERE usuarios.usuario = ?

        ORDER BY aulas.id DESC
    """, (usuario,))


    resultado = cursor.fetchall()


    conexao.close()

    return resultado



# ======================
# RESUMO DO ALUNO
# ======================


def resumo_aluno(usuario):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT id, nome
        FROM usuarios
        WHERE usuario = ?
    """, (usuario,))


    aluno = cursor.fetchone()


    if aluno is None:

        conexao.close()
        return None


    aluno_id = aluno[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM aulas
        WHERE aluno_id = ?
    """, (aluno_id,))


    quantidade = cursor.fetchone()[0]


    cursor.execute("""
        SELECT data, conteudo, observacao

        FROM aulas

        WHERE aluno_id = ?

        ORDER BY id DESC

        LIMIT 1

    """, (aluno_id,))


    ultima = cursor.fetchone()


    conexao.close()


    return {
        "nome": aluno[1],
        "quantidade": quantidade,
        "ultima_aula": ultima
    }



# ======================
# ATIVIDADES
# ======================


def adicionar_atividade(aluno_id, titulo, descricao):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        INSERT INTO atividades
        (aluno_id, titulo, descricao, status)

        VALUES (?, ?, ?, ?)

    """, (
        aluno_id,
        titulo,
        descricao,
        "Pendente"
    ))


    conexao.commit()
    conexao.close()



def buscar_atividades_aluno(usuario):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        SELECT
            atividades.id,
            atividades.titulo,
            atividades.descricao,
            atividades.status

        FROM atividades

        INNER JOIN usuarios

        ON atividades.aluno_id = usuarios.id

        WHERE usuarios.usuario = ?

        ORDER BY atividades.id DESC

    """, (usuario,))


    resultado = cursor.fetchall()


    conexao.close()

    return resultado



def concluir_atividade(id_atividade):

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
        UPDATE atividades

        SET status = 'Concluída'

        WHERE id = ?

    """, (id_atividade,))


    conexao.commit()
    conexao.close()
