import pickle
import gunicorn
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from utils.util import Utilities
from frontend.app_functions import App_Functions

func = App_Functions()
util = Utilities()
html_string='''
    <script language="javascript">
    alert("Thank You for visiting my project-Vignesh S")
    </script>
    '''
fraud_model = util.load_model("model/fraud_log_model.pkl")
flagged_fraud_model = util.load_model('model/flagged_fraud_log_model.pkl')
data = util.read_input('data/Fraud.csv')


def main():
    st.set_page_config(page_title="Transaction fraud detector",page_icon="data/bank.jpg",layout="centered",initial_sidebar_state="auto",menu_items=None)
    st.image("data/bank.jpg")
    st.title("Bank Transaction fraud and flagged fraud predictor")
    components.html(html_string)    
    st.markdown("<ht styl='text-align:center; color: Black;'>Chennai House SalesPrice and Overall Price</hr>",unsafe_allow_html=True)
    transaction_unicode, amount, cus_before_transaction, cus_after_transaction, rec_before_transaction, rec_after_transaction = func.get_prediction_data(data)
    prediction_value = pd.DataFrame([[transaction_unicode, int(amount), int(cus_before_transaction), int(cus_after_transaction), int(rec_before_transaction), int(rec_after_transaction)]], columns= ['type','amount', 'oldbalanceOrg','newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'],index = ['index'])
    fraud = fraud_model.predict(prediction_value)
    flagged_fraud = flagged_fraud_model.predict(prediction_value)
    print(type(fraud[0]))
    if st.button("Fraud Detection", help = "Click for fraud detection"):
        if fraud[0] == 1:
            st.markdown("<h1 style='text-align: center; color: grey;'>The transaction is found to be fraud</h1>", unsafe_allow_html=True)
            st.balloons()

        else:
            st.markdown("<h1 style='text-align: center; color: grey;'>The transaction is not found to be fraud</h1>", unsafe_allow_html=True)
            st.balloons()

    if st.button("Flagged Fraud Detection", help = "Click for flagged fraud detection"):
        if flagged_fraud[0] == 1:
            st.markdown("<h1 style='text-align: center; color: grey;'>The transaction is found to be flagged fraud</h1>", unsafe_allow_html=True)
            st.balloons()

        else:
            st.markdown("<h1 style='text-align: center; color: grey;'>The transaction is not found to be flagged fraud</h1>", unsafe_allow_html=True)
            st.balloons()
              
    if st.button("Like",help="Click to Like the Prediction"):
      st.write("Thanks for Liking the project")

if __name__=='__main__':
    main()