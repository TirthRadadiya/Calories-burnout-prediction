from flask import Flask
from cbp.exception import HousingException
from cbp.logger import logging

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        logging.INFO("Logging is working and we are in try block")
        raise Exception("This is trial Exception")
    except Exception as e:
        # logging.INFO("loggin in Except block")
        raise HousingException(e, sys) from 
    return "Starting of Machine Learning End to End Project"


if __name__=="__main__":
    app.run(debug=True)