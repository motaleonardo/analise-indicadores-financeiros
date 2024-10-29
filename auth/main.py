import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta_nome, consulta_geral, add_registro, create_table

COOKIE_EXPIRE_DAYS = 30

def main():

    try:
        consulta_geral()
    except:
        create_table()

    db_query = consulta_geral()

    registros = { 'usernames' : {} }
    for data in db_query:
        registros['usernames'][data[1]] = {
            'name': data[0],
            'password': data[2]
        }
    
    authenticator = stauth.Authenticate(
        registros,
        'random_coockie_name',
        'random_signature_key',
        COOKIE_EXPIRE_DAYS,
    )

    if 'onClickLogin' not in st.session_state:
        st.session_state['onClickLogin'] = False
    
    if st.session_state['onClickLogin'] == False:
        login_form(authenticator)
    else:
        user_form()


def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        authenticator.logout('Logout', main)
        st.title('Area do Dashboard') # Quando eu finalizar o meu dash aqui é que eu chamo ele
        st.write(f'Olá {name}, você está logado como {username}')
    elif authentication_status == False:
        st.write('Usuário ou senha inválidos, caso não tenha cadastro, entre em contato com o administrador')
    elif authentication_status == None:
        st.warning('Olá, faça seu login para acessar o dashboard')
        onClickLogin = st.button('Registrar')
        if onClickLogin:
            st.session_state['onClickLogin'] = True
            st.rerun()

def confirm_msg():
    hashed_password = stauth.Hasher([st.session_state.password]).generate()
    if st.session_state.password != st.session_state.confirm_password:
        st.warning('Senhas não conferem')
    elif consulta_nome():
        st.warning('Nome do usuário já existe')
    else:
        add_registro()
        st.success('Registro Efetuado!')

def user_form():
    with st.form(key='my_form', clear_on_submit=True):
        name = st.text_input('Nome', key='name')
        username = st.text_input('Usuário', key='user')
        password = st.text_input('Senha', type='password', key='password')
        confirm_password = st.text_input('Confirme a senha', type='password', key='confirm_password')
        submit_button = st.form_submit_button(
            "Salvar", on_click=confirm_msg,
        )
    onClickForm = st.button('Fazer Login')
    if onClickForm:
        st.session_state['onClickLogin'] = False
        st.rerun()



if __name__ == "__main__":
    main()