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
    resumo_aluno,
    proteger_senha
)


# Configuração

st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)


criar_tabelas()



# Sessão

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tipo_usuario" not in st.session_state:
    st.session_state.tipo_usuario = None



def logout():

    st.session_state.usuario_logado = None
    st.session_state.tipo_usuario = None



# Criar professora padrão

if buscar_usuario("professora") is None:

    adicionar_usuario(
        "Professora",
        "professora",
        "1234",
        "professor"
    )



# Cabeçalho

st.title("📚 ClassHub")

st.write(
    "Sistema de gerenciamento de aulas particulares"
)



# Sidebar

st.sidebar.title("Menu")


if st.session_state.usuario_logado:

    st.sidebar.write(
        f"Logado: {st.session_state.usuario_logado}"
    )


    if st.sidebar.button("Sair"):

        logout()
        st.rerun()



opcao = st.sidebar.selectbox(
    "Escolha uma opção:",
    [
        "Início",
        "Área do Professor",
        "Área do Aluno"
    ]
)



# =====================
# INÍCIO
# =====================

if opcao == "Início":

    st.header(
        "Bem-vindo ao ClassHub"
    )


    st.write(
        """
        Plataforma para organização de aulas particulares.

        Funcionalidades:

        - Cadastro de alunos
        - Cadastro de aulas
        - Histórico de aulas
        - Acompanhamento de evolução
        """
    )



# =====================
# PROFESSOR
# =====================

elif opcao == "Área do Professor":


    st.header(
        "👩‍🏫 Área do Professor"
    )


    if st.session_state.tipo_usuario == "professor":

        professor_logado = True

    else:

        senha = st.text_input(
            "Digite a senha:",
            type="password"
        )


        professora = buscar_usuario(
            "professora"
        )


        professor_logado = (
            professora
            and proteger_senha(senha) == professora[3]
        )


        if professor_logado:

            st.session_state.usuario_logado = professora[2]
            st.session_state.tipo_usuario = professora[4]

            st.success(
                "Login realizado!"
            )


    if professor_logado:


        opcao_professor = st.selectbox(
            "Escolha uma opção:",
            [
                "Cadastrar aluno",
                "Ver alunos",
                "Cadastrar aula",
                "Ver aulas"
            ]
        )


        # Cadastro aluno

        if opcao_professor == "Cadastrar aluno":


            nome = st.text_input(
                "Nome do aluno"
            )


            usuario = st.text_input(
                "Usuário"
            )


            senha = st.text_input(
                "Senha",
                type="password"
            )


            if st.button("Cadastrar"):


                adicionar_usuario(
                    nome,
                    usuario,
                    senha,
                    "aluno"
                )


                st.success(
                    "Aluno cadastrado com sucesso!"
                )



        # Lista alunos

        elif opcao_professor == "Ver alunos":


            st.subheader(
                "👥 Alunos cadastrados"
            )


            alunos = listar_alunos()


            if alunos:

                for aluno in alunos:

                    st.write(
                        f"👤 {aluno[0]} | Usuário: {aluno[1]}"
                    )

            else:

                st.info(
                    "Nenhum aluno cadastrado."
                )



        # Criar aula

        elif opcao_professor == "Cadastrar aula":


            st.subheader(
                "📚 Cadastrar aula"
            )


            alunos = listar_alunos_com_id()


            if alunos:


                alunos_dict = {
                    aluno[1]: aluno[0]
                    for aluno in alunos
                }


                aluno = st.selectbox(
                    "Escolha o aluno:",
                    alunos_dict.keys()
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
                        alunos_dict[aluno],
                        data,
                        conteudo,
                        observacao
                    )


                    st.success(
                        "Aula salva!"
                    )


            else:

                st.info(
                    "Nenhum aluno cadastrado."
                )



        # Ver aulas

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

----------------
"""
                    )


            else:

                st.info(
                    "Nenhuma aula cadastrada."
                )



# =====================
# ALUNO
# =====================

elif opcao == "Área do Aluno":


    st.header(
        "🎓 Área do Aluno"
    )


    if st.session_state.tipo_usuario == "aluno":


        usuario = st.session_state.usuario_logado


        resumo = resumo_aluno(
            usuario
        )


        st.success(
            f"Bem-vindo, {usuario}!"
        )


        if resumo:


            st.subheader(
                "📊 Meu progresso"
            )


            st.write(
                f"📚 Aulas realizadas: {resumo['quantidade']}"
            )


            if resumo["ultima_aula"]:


                st.write(
                    """
📝 Última aula:
"""
                )


                st.write(
                    f"""
📅 Data: {resumo['ultima_aula'][0]}

📖 Conteúdo: {resumo['ultima_aula'][1]}

📝 Observação: {resumo['ultima_aula'][2]}
"""
                )



        st.subheader(
            "📚 Todas minhas aulas"
        )


        aulas = buscar_aulas_por_usuario(
            usuario
        )


        if aulas:


            for aula in aulas:

                st.write(
                    f"""
📅 {aula[0]}

📖 {aula[1]}

📝 {aula[2]}

----------------
"""
                )


        else:

            st.info(
                "Você ainda não possui aulas cadastradas."
            )



    else:


        usuario = st.text_input(
            "Usuário"
        )


        senha = st.text_input(
            "Senha",
            type="password"
        )


        if st.button("Entrar"):


            aluno = buscar_usuario(
                usuario
            )


            if aluno and proteger_senha(senha) == aluno[3] and aluno[4] == "aluno":


                st.session_state.usuario_logado = aluno[2]
                st.session_state.tipo_usuario = aluno[4]

                st.rerun()


            else:

                st.error(
                    "Usuário ou senha incorretos."
                )
