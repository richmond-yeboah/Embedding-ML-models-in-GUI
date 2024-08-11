import streamlit as st

def main():
    st.set_page_config(
        page_title="Telco Customer Churn Prediction",
        page_icon="🔮",
        layout="wide"
    )

    st.title("Telco Customer Churn Prediction App")

    # Introduction
    st.write("""
        ## Welcome to the Telco Churn Prediction App!
        This application is designed to help you understand customer churn in the telecommunications industry. 
        Using machine learning, we aim to predict which customers are likely to leave based on various factors.
        """)

    # Project Description
    st.write("""
    ### Project Overview
    Customer churn is a significant issue in the telecom industry, where companies lose a portion of their customers to competitors. 
    In this app, we use a dataset from a telecom company to build a predictive model that identifies customers who are at risk of churning.""")

    # Navigation buttons (optional)
    st.write("### Explore the App")

    if st.button("🏠home"):
        st.write("Navigate to home page")

    if st.button("💾data"):
        st.write("Navigate to data page")

    if st.button("📜history"):
        st.write("Navigate to history page")

    if st.button("🔮prediction"):
        st.write("Navigate to prediction page")


    # Footer
    st.write("### About")
    st.info("This app was built using Streamlit as part of a Telco Churn Classification project.")

if __name__ == "__main__":
    main()