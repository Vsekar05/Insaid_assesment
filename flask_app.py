import traceback

from backend.api_functions import Api_functions
from utils.log import get_logger
from utils.util import Utilities
from utils.read_config import Config

from datetime import datetime
from waitress import serve
from flask import Flask, request
from flask_cors import CORS

import warnings
warnings.filterwarnings("ignore")

logger  = get_logger()
config = Config()
backend = Api_functions()
util = Utilities()
fraud_model = util.load_model("model/fraud_log_model.pkl")
flagged_fraud_model = util.load_model('model/flagged_fraud_log_model.pkl')

app = Flask(__name__)

def get_request(request:request) -> tuple[str, int, int, int, int, int]:
    """Getting requests from flask"""
    try:
        logger.info('Getting flask requests')
        type = request.form['Transaction type'].upper()
        amount = int(request.form['Amount'])
        cus_bef_balance = int(request.form['Customer balance before transaction'])
        cus_aft_balance = int(request.form['Customer balance after transaction'])
        rec_bef_balance = int(request.form['Recipient balance before transaction'])
        rec_aft_balance = int(request.form['Recipient balance before transaction'])
        logger.info('Flask requests arrived')
        return type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance
    except:
        logger.error('error in Getting request') 
        logger.critical(traceback.format_exc())


@app.route('/fraud_predictor', methods = ['POST'])
def fraud_detector():
    """Fraud detector api"""
    try:
        logger.critical("time:{}".format(datetime.now()))
        type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance = get_request(request)
        print(type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance)
        fraud_final_output = backend.identify_fraud(fraud_model, type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance)
        print(fraud_final_output)
        logger.critical("completed services")
        return fraud_final_output
    except Exception:
        service_err = util.service_error('error in application')
        logger.critical(service_err)
        logger.critical(traceback.format_exc())
        
        return service_err

@app.route('/flagged_fraud_predictor', methods = ['POST'])
def flagged_fraud_detector():
    """Flagged Fraud detector api"""
    try:
        logger.critical("time:{}".format(datetime.now()))
        type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance = get_request(request)
        fraud_final_output = backend.identify_flagged_fraud(flagged_fraud_model, type, amount, cus_bef_balance, cus_aft_balance, rec_bef_balance, rec_aft_balance)
        logger.critical("completed services")
        return fraud_final_output
    except Exception:
        service_err = util.service_error('error in application')
        logger.critical(service_err)
        logger.critical(traceback.format_exc())
        return service_err
    
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8003)