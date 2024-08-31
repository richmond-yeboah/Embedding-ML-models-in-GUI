import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def login_user():
    # Load the configuration from config.yaml
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize the authenticator with credentials and cookie settings
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # Layout for login
    col1, col2, col3 = st.columns([.3, .4, .3])
    with col2:
        name, authentication_status, username = authenticator.login('Login', 'main')

        # Debugging outputs
        st.write(f"Authentication Status: {authentication_status}")
        st.write(f"Username: {username}")
        st.write(f"Name: {name}")

        if authentication_status:
            with st.sidebar:
                authenticator.logout('Logout', 'sidebar')
            st.success(f'Welcome {name}')
        elif authentication_status is False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')

if __name__ == '__main__':
    login_user()

