import streamlit as st
import pandas as pd
import numpy as np
from login import login_user


# Configure the page
st.set_page_config(
    page_title='Data Viewer',
    page_icon='👨‍💻',
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

def data_page():

    #login_user()
    #if st.session_state["authentication_status"] == True:

        # Set header for dataset view
        st.title('Dataset View')

            # Create selection option
        column1, column2 = st.columns(2)
        with column2:
                    option = st.selectbox('Choose columns to be viewed',
                                        ('All Columns','Numeric Columns','Categorical Columns'))

            # ---- Load remote dataset
        @st.cache_data(show_spinner='Loading data')
        def load_data():
            df = pd.read_csv('https://github.com/richmond-yeboah/Customer-Churn-Prediction/raw/main/Data/Telco.csv')
            return df

        df = load_data().head(100)

            # Display based on selection
        if option == 'Numeric Columns':
            st.subheader('Numeric Columns')
            st.write(df.select_dtypes(include='number'))

        elif option == 'Categorical Columns':
            st.subheader('Categorical Columns')
            st.write(df.select_dtypes(include='object'))

        else:
            st.subheader('Complete Dataset')
            st.write(df)


            # ----- Add column descriptions of the dataset
        with st.expander('**Click to view column description**'):
            st.markdown('''
                :gray[**The following describes the columns present in the data.**]

            **Gender** -- Whether the customer is a male or a female

            **SeniorCitizen** -- Whether a customer is a senior citizen or not

            **Partner** -- Whether the customer has a partner or not (Yes, No)

            **Dependents** -- Whether the customer has dependents or not (Yes, No)

            **Tenure** -- Number of months the customer has stayed with the company

            **Phone Service** -- Whether the customer has a phone service or not (Yes, No)

            **MultipleLines** -- Whether the customer has multiple lines or not

            **InternetService** -- Customer's internet service provider (DSL, Fiber Optic, No)

            **OnlineSecurity** -- Whether the customer has online security or not (Yes, No, No Internet)

            **OnlineBackup** -- Whether the customer has online backup or not (Yes, No, No Internet)

            **DeviceProtection** -- Whether the customer has device protection or not (Yes, No, No internet service)

            **TechSupport** -- Whether the customer has tech support or not (Yes, No, No internet)

            **StreamingTV** -- Whether the customer has streaming TV or not (Yes, No, No internet service)

            **StreamingMovies** -- Whether the customer has streaming movies or not (Yes, No, No Internet service)

            **Contract** -- The contract term of the customer (Month-to-Month, One year, Two year)

            **PaperlessBilling** -- Whether the customer has paperless billing or not (Yes, No)

            **Payment Method** -- The customer's payment method (Electronic check, mailed check, Bank transfer(automatic), Credit card(automatic))

            **MonthlyCharges** -- The amount charged to the customer monthly

            **TotalCharges** -- The total amount charged to the customer

            **Churn** -- Whether the customer churned or not (Yes or No)
            ''')
             
if __name__ == '__main__':
    data_page()