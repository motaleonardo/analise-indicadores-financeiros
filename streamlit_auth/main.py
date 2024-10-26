import streamlit as st
from streamlit_authenticator import stauth

COOKIE_EXPIRE_DAYS = 30

def main():
    authenticator = stauth.Authenticator(
        {'username': {'teste':{'name': 'testando', 'password': 'blabla'}}},
        'random_coockie_name',
        'random_signature_key',

        COOKIE_EXPIRE_DAYS,
    )

    if 'onClick' not in st.session_state:
        st.session_state['onClick'] = False

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
        onClick = st.button('Login')
        if onClick:
            st.session_state['onClick'] = True

if __name__ == '__main__':
    main()