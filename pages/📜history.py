import streamlit as st
import pandas as pd
from login import login_user


# Configure the page
st.set_page_config(
    page_title='History',
    page_icon='📜',
    layout='wide'
)


# --------- Add custom CSS to adjust the width of the sidebar
st.markdown( """ <style> 
            section[data-testid="stSidebar"]
            { width: 200px !important;
            }
            </style> """,
            unsafe_allow_html=True,
)

def history_page():
        
    # login_user()
    # if st.session_state["authentication_status"] == True:
        # Set header for page
        st.title('History')

        data = pd.read_csv('./data/history.csv')
        st.dataframe(data)

if __name__ == '__main__':
    history_page()