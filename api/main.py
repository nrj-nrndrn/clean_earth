#main.py
from flask import Flask, jsonify, request
from db import details, classify, classify_prod,points
app = Flask(__name__)

@app.route('/classify', methods=['POST', 'GET'])
def classify_items():
    if request.method == 'POST':
     #   if not request.is_json:
      #      return jsonify({"msg": "Missing JSON in request"}), 400
        classify(["Coca Cola", "2lb organic", "Strawberries"])


@app.route('/details', methods=['GET'])
def get_details():
    return details()

@app.route('/points', methods=['GET'])
def get_points():
    return points()

@app.route('/details_products', methods=['POST'])
def get_detail_products():
    obj = {'Coca Cola','Pepsi'}
    return classify_prod(request.get_json())

if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8877')

