import streamlit as st
from database import carregar_usuarios

# Carregar usuários
import streamlit as st
from database import carregar_usuarios


usuarios = carregar_usuarios()


usuarios = carregar_usuarios()
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

        st.write("Painel do professor em construção.")

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
