import streamlit as st

def main():
    st.set_page_config(
        page_title="Telco Customer Churn Prediction",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state='auto'
    )

    st.title("Telco Customer Churn Prediction App")

    # Introduction
    st.write("""
        ## Welcome to the Telco Churn Prediction App!
        This application is designed to help you understand customer churn in the telecommunications industry. 
        Using machine learning, we aim to predict which customers are likely to leave based on various factors.
        """)

    cols = st.columns(2)
        # Churn Prediction Status
    with cols[0]:
        st.subheader('Churn Prediction Status')
        st.write("This application provides a platform for predicting the churn status of customers by leveraging historical data encompassing customer demographics, subscription details, account information, and their corresponding churn status.")

        # Application Features
    with cols[0]:
        st.subheader('Application Features')
        st.markdown("""                
            * Data - View proprietory data
            * Dashboard - Shows EDA and KPIs with other analytical questions
            * Prediction - Allows user to predict churn status from two available models
            * History - Displays all previous predictions made using the app
            """)

    # Key Advantages
    with cols[0]:
        st.subheader('Key Advantages')
        st.markdown("""
                    Discover the advantages of using this Churn Prediction App, such as;
                    * Accurate predictions
                    * User-friendly interface
                    """)

    # How to run the app
    with cols[1]:
        st.subheader('How to Run the App')
        st.write("Follow the steps to run the Customer Churn Prediction App and make accurate predictions for customer churn.")
        st.code("""
                    #activate virtual environment
                    venv/Scripts/activate

                    streamlit run 🏠home.py
                    """, language="python")

        # Machine Learning Integration
    with cols[1]:
        st.subheader('Machine Learning Integration')
        st.write("Learn about the machine learning models integrated into the app, including Gradient Boosting and Support Vector models.")

        # Need Assistance
    with cols[1]:
        st.subheader('Contact Information')
        st.write("Feel free to reach out. Email: richmondyeboah299@gmail.com")
        cols = st.columns(4)

        with cols[0]:
            st.link_button(":red[GitHub]", "https://github.com/richmond-yeboah/Embedding-ML-models-in-GUI")
        with cols[2]:
            st.link_button(":red[LinkedIn]", "https://www.linkedin.com/in/richmond-yeboah-")


    # Footer
    st.write("### About")
    st.info("This app was built using Streamlit as part of a Telco Churn Classification project.")

if __name__ == "__main__":
    main()