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

    conexao.commit()
    conexao.close()


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


def atualizar_senha(usuario, nova_senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE usuario = ?
    """, (
        proteger_senha(nova_senha),
        usuario
    ))

    conexao.commit()
    conexao.close()


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


def listar_aulas_aluno(aluno_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT data, conteudo, observacao
        FROM aulas
        WHERE aluno_id = ?
    """, (aluno_id,))

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

import streamlit as st

from database import (
    criar_tabelas,
    adicionar_usuario,
    buscar_usuario,
    listar_alunos,
    listar_alunos_com_id,
    adicionar_aula,
    listar_todas_aulas,
    buscar_aulas_por_usuario,
    proteger_senha
)


criar_tabelas()


# Controle de sessão

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tipo_usuario" not in st.session_state:
    st.session_state.tipo_usuario = None


def logout():

    st.session_state.usuario_logado = None
    st.session_state.tipo_usuario = None



st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)



# Criar professora padrão

if buscar_usuario("professora") is None:

    adicionar_usuario(
        "Professora",
        "professora",
        "1234",
        "professor"
    )



st.title("📚 ClassHub")

st.write(
    "Sistema de gerenciamento de aulas particulares"
)



# Mostrar sessão

if st.session_state.usuario_logado:

    st.sidebar.write(
        f"Logado: {st.session_state.usuario_logado}"
    )

    if st.sidebar.button("Sair"):

        logout()
        st.rerun()



st.sidebar.title("Menu")


opcao = st.sidebar.selectbox(
    "Escolha uma opção:",
    [
        "Início",
        "Área do Professor",
        "Área do Aluno"
    ]
)



# Início

if opcao == "Início":

    st.header("Bem-vindo ao ClassHub")

    st.write(
        """
        Plataforma para organização de aulas particulares.

        Aqui você poderá:

        - Gerenciar alunos
        - Criar atividades
        - Acompanhar evolução
        - Organizar materiais
        """
    )



# Professor

elif opcao == "Área do Professor":

    st.header("👩‍🏫 Área do Professor")


    senha = st.text_input(
        "Digite a senha:",
        type="password"
    )


    professora = buscar_usuario("professora")


    if professora and proteger_senha(senha) == professora[3]:

        st.session_state.usuario_logado = professora[1]
        st.session_state.tipo_usuario = professora[4]


        st.success(
            "Login realizado!"
        )


        opcao_professor = st.selectbox(
            "Escolha uma opção:",
            [
                "Cadastrar aluno",
                "Ver alunos",
                "Cadastrar aula",
                "Ver aulas"
            ]
        )


        if opcao_professor == "Cadastrar aluno":

            nome = st.text_input(
                "Nome do aluno"
            )


            usuario = st.text_input(
                "Usuário"
            )


            senha_aluno = st.text_input(
                "Senha do aluno",
                type="password"
            )


            if st.button("Cadastrar"):

                adicionar_usuario(
                    nome,
                    usuario,
                    senha_aluno,
                    "aluno"
                )

                st.success(
                    "Aluno cadastrado com sucesso!"
                )



        elif opcao_professor == "Ver alunos":

            st.subheader(
                "👥 Alunos cadastrados"
            )


            alunos = listar_alunos()


            if alunos:

                for aluno in alunos:

                    st.write(
                        f"👤 {aluno[0]} - Usuário: {aluno[1]}"
                    )

            else:

                st.info(
                    "Nenhum aluno cadastrado."
                )



        elif opcao_professor == "Cadastrar aula":

            st.subheader(
                "📚 Cadastrar aula"
            )


            alunos = listar_alunos_com_id()


            if alunos:

                nomes_alunos = {
                    aluno[1]: aluno[0]
                    for aluno in alunos
                }


                aluno_escolhido = st.selectbox(
                    "Escolha o aluno:",
                    nomes_alunos.keys()
                )


                data = st.text_input(
                    "Data da aula"
                )


                conteudo = st.text_input(
                    "Conteúdo estudado"
                )


                observacao = st.text_area(
                    "Observações"
                )


                if st.button("Salvar aula"):

                    adicionar_aula(
                        nomes_alunos[aluno_escolhido],
                        data,
                        conteudo,
                        observacao
                    )


                    st.success(
                        "Aula cadastrada com sucesso!"
                    )


            else:

                st.info(
                    "Cadastre um aluno primeiro."
                )



        elif opcao_professor == "Ver aulas":

            st.subheader(
                "📚 Histórico de aulas"
            )


            aulas = listar_todas_aulas()


            if aulas:

                for aula in aulas:

                    st.write(
                        f"""
👤 Aluno: {aula[0]}

📅 Data: {aula[1]}

📖 Conteúdo: {aula[2]}

📝 Observação: {aula[3]}

---
"""
                    )

            else:

                st.info(
                    "Nenhuma aula cadastrada."
                )



    elif senha:

        st.error(
            "Senha incorreta."
        )



# Aluno

elif opcao == "Área do Aluno":

    st.header(
        "🎓 Área do Aluno"
    )


    usuario = st.text_input(
        "Usuário"
    )


    senha = st.text_input(
        "Senha",
        type="password"
    )


    if st.button("Entrar"):

        aluno = buscar_usuario(usuario)


        if aluno and proteger_senha(senha) == aluno[3] and aluno[4] == "aluno":

            st.session_state.usuario_logado = aluno[1]
            st.session_state.tipo_usuario = aluno[4]

            st.rerun()


        else:

            st.error(
                "Usuário ou senha incorretos."
            )



# Painel do aluno logado

if (
    st.session_state.tipo_usuario == "aluno"
):

    st.header(
        "🎓 Área do Aluno"
    )


    st.success(
        f"Bem-vindo, {st.session_state.usuario_logado}!"
    )


    st.subheader(
        "📚 Minhas aulas"
    )


    aulas = buscar_aulas_por_usuario(
        st.session_state.usuario_logado
    )


    if aulas:

        for aula in aulas:

            st.write(
                f"""
📅 Data: {aula[0]}

📖 Conteúdo: {aula[1]}

📝 Observação: {aula[2]}

---
"""
            )

    else:

        st.info(
            "Você ainda não possui aulas cadastradas."
        )
