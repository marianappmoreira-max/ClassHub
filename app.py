import streamlit as st

from database import (
    criar_tabelas,
    adicionar_usuario,
    buscar_usuario,
    listar_alunos,
    listar_alunos_com_id,
    adicionar_aula,
    listar_todas_aulas,
    proteger_senha
)


criar_tabelas()


# Configuração da página
st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)


# Criar professora padrão caso não exista
if buscar_usuario("professora") is None:

    adicionar_usuario(
        "Professora",
        "professora",
        "1234",
        "professor"
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

    senha = st.text_input(
        "Digite a senha:",
        type="password"
    )


    professora = buscar_usuario("professora")


    if professora and proteger_senha(senha) == professora[3]:

        st.success("Login realizado!")

        st.subheader("Painel do Professor")


        opcao_professor = st.selectbox(
            "Escolha uma opção:",
            [
                "Cadastrar aluno",
                "Ver alunos",
                "Cadastrar aula",
                "Ver aulas"
            ]
        )


        # Cadastro de aluno
        if opcao_professor == "Cadastrar aluno":

            nome = st.text_input("Nome do aluno")

            usuario = st.text_input("Usuário")

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


        # Ver alunos
        elif opcao_professor == "Ver alunos":

            st.subheader("Alunos cadastrados")

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


        # Cadastrar aula
        elif opcao_professor == "Cadastrar aula":

            st.subheader("📚 Cadastrar aula")


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


        # Ver aulas
        elif opcao_professor == "Ver aulas":

            st.subheader("📚 Histórico de aulas")


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

        st.error("Senha incorreta.")



# Área do aluno
elif opcao == "Área do Aluno":

    st.header("🎓 Área do Aluno")

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

            st.success(
                f"Bem-vindo, {aluno[1]}!"
            )

            st.write(
                "Área do aluno em construção."
            )


        else:

            st.error(
                "Usuário ou senha incorretos."
            )
            )
