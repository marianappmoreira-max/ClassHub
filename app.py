import streamlit as st

from database import (
    criar_tabelas,
    adicionar_usuario,
    buscar_usuario,
    listar_alunos
)


criar_tabelas()
# Configuração da página
st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)

# Título
st.title("📚 ClassHub")
st.write("Sistema de gerenciamento de aulas particulares")

# Menu inicial
st.sidebar.title("Menu")

opcao = st.sidebar.selectbox(
    "Escolha uma opção:",
    [
        "Início",
        "Área do Professor",
        "Área do Aluno"
    ]
)

# Página inicial
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

# Área do professor
elif opcao == "Área do Professor":
    st.header("👩‍🏫 Área do Professor")
    st.write("Área exclusiva da professora.")

    senha = st.text_input(
        "Digite a senha:",
        type="password"
    )

    if senha == usuarios["professora"]["senha"]:
        st.success("Login realizado!")

        st.subheader("Painel do Professor")

        opcao_professor = st.selectbox(
            "Escolha uma opção:",
            [
                "Cadastrar aluno",
                "Ver alunos"
            ]
        )

        if opcao_professor == "Cadastrar aluno":

            nome = st.text_input("Nome do aluno")
            usuario = st.text_input("Usuário")
            senha_aluno = st.text_input(
                "Senha do aluno",
                type="password"
            )

            if st.button("Cadastrar"):

                novo_aluno = {
                    "nome": nome,
                    "usuario": usuario,
                    "senha": senha_aluno,
                    "tipo": "aluno"
                }

                usuarios["alunos"].append(novo_aluno)

                from database import salvar_usuarios
                salvar_usuarios(usuarios)

                st.success("Aluno cadastrado com sucesso!")

    elif senha:
        st.error("Senha incorreta.")

# Área do aluno
elif opcao == "Área do Aluno":
    st.header("🎓 Área do Aluno")

    usuario = st.text_input("Usuário")
    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        if usuario and senha:
            st.success("Login realizado!")
            st.write("Área do aluno em construção.")

        else:
            st.warning("Preencha todos os campos.")
