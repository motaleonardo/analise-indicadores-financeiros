import re
from datetime import datetime
import streamlit as st
import streamlit_authenticator as stauth
from time import sleep
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
        registros['usernames'][data[2]] = {
            'name': data[1],
            'password': data[3]
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
        authenticator.logout('Logout', 'main')
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
    allowed_domains = ["@casadopicapau.com.br", "@grupoluizhohl.com.br"]
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    email = st.session_state.email
    password = st.session_state.password
    confirm_password = st.session_state.confirm_password

    # Check if email domain is allowed
    if not any(email.endswith(domain) for domain in allowed_domains):
        st.warning('Dominio de Email não permitido!')
        sleep(3)
        return

    # Check if passwords match
    if password != confirm_password:
        st.warning('Senhas não conferem!')
        sleep(3)
        return

    # Validate password complexity
    if (len(password) < 8 or
        not re.search(r'[A-Z]', password) or
        not re.search(r'[a-z]', password) or
        not re.search(r'[0-9]', password) or
        not any(char in special_characters for char in password)):
        st.warning('Senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial!')
        sleep(3)
        return

    # Check if username already exists
    if consulta_nome(st.session_state.user):
        st.warning('Nome do usuário já existe!')
        sleep(3)
        return

    # Hash the password and add the user to the database
    hashed_password = stauth.Hasher([password]).generate()
    current_time = datetime.now()
    add_registro(st.session_state.name, st.session_state.user, hashed_password[0], email, current_time)
    st.success('Registro Efetuado!')
    sleep(3)

def user_form():
    with st.form(key='my_form', clear_on_submit=True):
        name = st.text_input('Nome', key='name')
        username = st.text_input('Usuário', key='user')
        email = st.text_input('E-mail', key='email')
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