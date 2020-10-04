import socket
from flask import Flask, request,render_template,jsonify
from flask_restplus import Resource, Api ,reqparse,Namespace,fields
import sys,requests


from flask_cors import CORS, cross_origin
from statistics import mean

import datetime
from datetime import timedelta
from datetime import datetime

from webargs.flaskparser import use_args

socket.getaddrinfo('localhost', 8080)

app = Flask(__name__)
#
# CORS(app)
#
# api = Api(app,version="1",title="Clean Earth",description="This web-app is ....")
# weatherAPI = Namespace('HistoricalWeather', description='Historical Weather')
# api.add_namespace(weatherAPI)
#
@app.route("/",methods=["GET","POST"])
# @api.doc(True)
def index():
    return render_template("index.html")

@app.route("/get_items",methods=["GET","POST"])
# @api.doc(responses={200: 'Available data retrieved successfully'})
def upload_bill():
    response = requests.get(
        "https://hackathon-cloud-291419.wl.r.appspot.com/details")
    response = response.json()
    return render_template("page2.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)






