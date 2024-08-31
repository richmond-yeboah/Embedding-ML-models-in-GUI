import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def login_user():

    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
    col1, col2, col3 = st.columns([.3,.4,.3])
    with col2:
        
        authenticator.login()
        
        if (st.session_state["authentication_status"] == True) or (st.session_state["authentication_status"] == False):
            with st.sidebar:
                authenticator.logout()
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

    
if __name__ == '__main__':
    login_user()