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
    adicionar_atividade,
    buscar_atividades_aluno,
    concluir_atividade,
    proteger_senha
)


st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)


criar_tabelas()


if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tipo_usuario" not in st.session_state:
    st.session_state.tipo_usuario = None



def logout():

    st.session_state.usuario_logado = None
    st.session_state.tipo_usuario = None



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



# =========================
# INÍCIO
# =========================

if opcao == "Início":

    st.header("Bem-vindo ao ClassHub")

    st.write(
        """
        Plataforma para organização de aulas particulares.

        Funcionalidades:

        - Cadastro de alunos
        - Cadastro de aulas
        - Atividades
        - Histórico
        - Acompanhamento de evolução
        """
    )



# =========================
# PROFESSOR
# =========================

elif opcao == "Área do Professor":

    st.header("👩‍🏫 Área do Professor")


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
                "Ver aulas",
                "Cadastrar atividade"
            ]
        )



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
    adicionar_atividade,
    buscar_atividades_aluno,
    concluir_atividade,
    proteger_senha
)


st.set_page_config(
    page_title="ClassHub",
    page_icon="📚",
    layout="centered"
)


criar_tabelas()


if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tipo_usuario" not in st.session_state:
    st.session_state.tipo_usuario = None



def logout():

    st.session_state.usuario_logado = None
    st.session_state.tipo_usuario = None



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



# =========================
# INÍCIO
# =========================

if opcao == "Início":

    st.header("Bem-vindo ao ClassHub")

    st.write(
        """
        Plataforma para organização de aulas particulares.

        Funcionalidades:

        - Cadastro de alunos
        - Cadastro de aulas
        - Atividades
        - Histórico
        - Acompanhamento de evolução
        """
    )



# =========================
# PROFESSOR
# =========================

elif opcao == "Área do Professor":

    st.header("👩‍🏫 Área do Professor")


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
                "Ver aulas",
                "Cadastrar atividade"
            ]
        )



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
