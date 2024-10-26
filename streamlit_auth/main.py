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
        st.session_state['onClickLogin'] = False
    
    if st.session_state['onClickLogin'] == False:
        login_form(authenticator)

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
        onClickLogin = st.button('Login')
        if onClickLogin:
            st.session_state['onClickLogin'] = True
            st.rerun()

def confirm_msg():
    hashed_password = stauth.Hasher([st.session_state.password]).generate()
    if st.session_state.password != st.session_state.confirm_password:
        st.warning('Senhas não conferem')
    elif 'consult_username':
        st.warning('Nome do usuário já existe')
        st.success('Registro Efetuado!')

def user_form():
    with st.form(key='my_form', clear_on_submit=True):
        name = st.text_input('Nome', key='name')
        username = st.text_input('Usuário', key='user')
        password = st.text_input('Senha', type='password', key='password')
        confirm_password = st.text_input('Confirme a senha', type='password', key='confirm_password')
        submit_button = st.form_submit_button(
            'Salvar', on_click=confirm_msg,
        )
        onClickForm = st.button('Fazer Login')
        if onClickForm:
            st.session_state['onClickLogin'] = False
            st.rerun()


if __name__ == '__main__':
    main()