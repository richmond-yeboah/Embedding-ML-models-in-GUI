import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (
    CredentialsError, ForgotError, Hasher, LoginError, RegisterError, ResetError, UpdateError
)

# Set up the page configuration
st.set_page_config(
    page_title="Sign Up",
    page_icon="assets/app_icon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Loading config file
with open('./config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Title and Instructions
st.title("Create a New Account")
st.write("""
Welcome to the Churn Predictor App registration page! Please fill out the form below to create a new account. 
Once registered, you will be able to log in and use the app.

Ensure that you provide valid credentials for your account. After successful registration, you will be directed to the Welcome page where you can proceed to log in.
""")

# Creating a new user registration widget
try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False, fields={'Form name': 'Sign Up Here', 'Register': 'Sign Up'})
    if email_of_registered_user:
        st.success('The new user has been successfully registered.')
        st.write("""
        Your account has been created successfully. You can now proceed to login. 
        Click [here](http://localhost:8501) to go to the Gateway page.
        """)
except RegisterError as e:
    st.error(f"Registration Error: {e}")

# Save the updated configuration file
with open('./config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)

# Additional UI elements
st.write("---")
st.write("Need help? Contact support at support@example.com")