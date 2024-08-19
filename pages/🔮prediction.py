import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import requests
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import imblearn
import os

# Configure the page
st.set_page_config(
    page_title='Predictions',
    page_icon='🔮',
    layout='wide'
)

st.title("Predict Customer Churn!")

column1, column2 = st.columns([.6, .4])
with column1:
    model_option = st.selectbox('Choose which model to use for prediction', options=['Gradient Boosting', 'Support Vector'])

# Load trained machine learning model and encoder from GitHub
# Load trained machine learning model and encoder from GitHub
    github_model1_url = 'https://raw.githubusercontent.com/richmond-yeboah/Telecom-Customer-Churn-Prediction/main/model/GradientBoosting.joblib'
    github_model2_url = 'https://raw.githubusercontent.com/richmond-yeboah/Telecom-Customer-Churn-Prediction/main/model/SupportVector.joblib'
    encoder_url = 'https://raw.githubusercontent.com/richmond-yeboah/Telecom-Customer-Churn-Prediction/main/model/label_encoder.joblib'

# -------- Function to load the model from GitHub
@st.cache_resource(show_spinner="Loading model")
def gb_pipeline():
    response = requests.get(github_model1_url)
    model_bytes = BytesIO(response.content)
    pipeline = joblib.load(model_bytes)
    return pipeline


@st.cache_resource(show_spinner="Loading model")
def sv_pipeline():
    response = requests.get(github_model2_url)
    model_bytes = BytesIO(response.content)
    pipeline = joblib.load(model_bytes)
    return pipeline


# --------- Function to load encoder from GitHub
def load_encoder():
    response = requests.get(encoder_url)
    encoder_bytes = BytesIO(response.content)
    encoder = joblib.load(encoder_bytes)
    return encoder


# --------- Create a function for model selection
def select_model():
    # ------- Option for first model
    if model_option == 'Gradient Boosting':
        model = gb_pipeline()
    # ------- Option for second model
    if model_option == 'Support Vector':
        model = sv_pipeline()
    encoder = load_encoder()
    return model, encoder


# Custom function to deal with cleaning the total charges column
class TotalCharges_cleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Replace empty string with NA
        X['TotalCharges'].replace(' ', np.nan, inplace=True)

        # Convert the values in the Totalcharges column to a float
        X['TotalCharges'] = X['TotalCharges'].transform(lambda x: float(x))
        return X
        
    # Serialization methods
    def __getstate__(self):
        # Return state to be serialized
        return {}

    def __setstate__(self, state):
        # Restore state from serialized data
        pass
        
    # Since this transformer doesn't remove or alter features, return the input features
    def get_feature_names_out(self, input_features=None):
        return input_features


# Create a class to deal with dropping Customer ID from the dataset
class columnDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Drop the specified column
        return X.drop('customerID', axis=1)
        
    def get_feature_names_out(self, input_features=None):
        # If input_features is None or not provided, return None
        if input_features is None:
            return None
        # Return feature names after dropping the specified column
        return [feature for feature in input_features if feature != 'customerID']

# ---- Initialize prediction in session state
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'prediction_proba' not in st.session_state:
    st.session_state['prediction_proba'] = None

# ------- Create a function to make prediction
def make_prediction(model, encoder):

    customerID = st.session_state['customer_id']
    gender = st.session_state['gender']
    SeniorCitizen = st.session_state['senior_citizen']
    Partner = st.session_state['partners']
    Dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    PhoneService = st.session_state['phone_service']
    MultipleLines = st.session_state['multiple_lines']
    InternetService = st.session_state['internet_service']
    OnlineSecurity = st.session_state['online_security']
    OnlineBackup = st.session_state['online_backup']
    DeviceProtection = st.session_state['device_protection']
    TechSupport = st.session_state['tech_support']
    StreamingTV = st.session_state['streaming_tv']
    StreamingMovies = st.session_state['streaming_movies']
    Contract = st.session_state['contract']
    PaperlessBilling = st.session_state['paperless_billing']
    PaymentMethod = st.session_state['payment_method']
    MonthlyCharges = st.session_state['monthly_charges']
    TotalCharges = st.session_state['total_charges']
        
    columns = ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
        
    values = [[customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
            MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
            TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
            PaymentMethod, MonthlyCharges, TotalCharges]]
        
    data = pd.DataFrame(values, columns=columns)

    # -------- Get the value for prediction
    prediction = model.predict(data)
    prediction = encoder.inverse_transform(prediction)
    st.session_state['prediction'] = prediction

    # -------- Get the value for prediction probability
    prediction_proba = model.predict_proba(data)
    st.session_state['prediction_proba'] = prediction_proba

    data['Churn'] = prediction
    data['Model'] = model_option

    data.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    return prediction, prediction_proba


# ------- Prediction page creation
def input_features():

    with st.form('features'):
        model_pipeline, encoder = select_model()
        col1, col2 = st.columns(2)

        # ------ Collect customer information
        with col1:
            st.subheader('Demographics')
            st.text_input('Customer ID', value="", placeholder='eg. 1234-ABCDE', key='customer_id')
            st.radio('Gender', options=['Male', 'Female'],horizontal=True, key='gender',)
            st.radio('Partners', options=['Yes', 'No'],horizontal=True, key='partners')
            st.radio('Dependents', options=['Yes', 'No'],horizontal=True, key='dependents')
            st.radio("Senior Citizen ('Yes-1, No-0')", options=[1, 0],horizontal=True, key='senior_citizen')
            
        # ------ Collect customer account information
        with col1:
            st.subheader('Customer Account Info.')
            st.number_input('Tenure', min_value=0, max_value=70, key='tenure')
            st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'], key='contract')
            st.selectbox('Payment Method',
                                        options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
                                        key='payment_method')
            st.radio('Paperless Billing', ['Yes', 'No'], horizontal=True, key='paperless_billing')
            st.number_input('Monthly Charges', placeholder='Enter amount...', key='monthly_charges')
            st.number_input('Total Charges', placeholder='Enter amount...', key='total_charges')
            
        # ------ Collect customer subscription information
        with col2:
            st.subheader('Subscriptions')
            st.radio('Phone Service', ['Yes', 'No'], horizontal=True, key='phone_service')
            st.selectbox('Multiple Lines', ['Yes', 'No', 'No internet servie'], key='multiple_lines')
            st.selectbox('Internet Service', ['DSL','Fiber optic', 'No'], key='internet_service')
            st.selectbox('Online Security', ['Yes', 'No', 'No internet servie'], key='online_security')
            st.selectbox('Online Backup', ['Yes', 'No', 'No internet servie'], key='online_backup')
            st.selectbox('Device Protection', ['Yes', 'No', 'No internet servie'], key='device_protection')
            st.selectbox('Tech Support', ['Yes', 'No', 'No internet servie'], key='tech_support')
            st.selectbox('Streaming TV', ['Yes', 'No', 'No internet servie'], key='streaming_tv')
            st.selectbox('Streaming Movies', ['Yes', 'No', 'No internet servie'], key='streaming_movies')
            
        st.form_submit_button('Predict', on_click=make_prediction, kwargs=dict(model=model_pipeline, encoder=encoder))

    return True
        

if __name__=='__main__':
    input_features()
    prediction = st.session_state['prediction']
    probability = st.session_state['prediction_proba']    

    if st.session_state['prediction'] == None:
        cols = st.columns([3, 4, 3])
        with cols[1]:
            st.markdown('#### Predictions will show here ⤵️')
        cols = st.columns([.25,.5,.25])
        with cols[1]:
            st.markdown('##### No predictions made yet. Make prediction')
    else:
        if prediction == "Yes":
            cols = st.columns([.1,.8,.1])
            with cols[1]:
                st.markdown(f'### The customer will churn with a {round(probability[0][1],2)} probability.')
            cols = st.columns([.3,.4,.3])
            with cols[1]:
                st.success('Churn status predicted successfullly🎉')
        else:
            cols = st.columns([.1,.8,.1])
            with cols[1]:
                st.markdown(f'### The customer will not churn with a {round(probability[0][0],2)} probability.')
            cols = st.columns([.3,.4,.3])
            with cols[1]:
                st.success('Churn status predicted successfullly🎉')