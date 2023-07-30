from flask import Flask, jsonify
from config_app import Api

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Welcome to the Dolar Venezuela API. Go to documentation: https://github.com/fcoagz/api-pydolarvenezuela</p>"

@app.route('/api/v1/dollar/unit/<string:key_monitor>', methods=["GET"])
def params_heard_key(key_monitor: str):
    return jsonify(Api().getMonitor(key_monitor))

@app.route('/api/v1/dollar/<string:section_dollar>', methods=["GET"])
def params_heard_section(section_dollar: str):
    return jsonify(Api().categorized(section_dollar))

@app.route('/api/v1/dollar/<string:section_dollar>/<string:key_monitor>', methods=["GET"])
def params_heard_section_and_key(section_dollar: str, key_monitor: str):
    return jsonify(Api().categorized(section_dollar, key_monitor))

@app.route('/api/v1/dollar/td/<string:value>/<string:key_monitor>', methods=["GET"])
def params_heard_toDollar(value: str, key_monitor: str):
    if value.isnumeric():
        price = Api().getDollar(key_monitor)
        return jsonify(float(value) * float(price)) if not type(price) == dict else price
    return jsonify({'message': f'Cannot GET information the value: {value}'})

@app.route('/api/v1/dollar/tb/<string:value>/<string:key_monitor>', methods=["GET"])
def params_heard_toBs(value: str, key_monitor: str):
    if value.isnumeric():
        price = Api().getDollar(key_monitor)
        return jsonify(float(value) / float(price)) if not type(price) == dict else price
    return jsonify({'message': f'Cannot GET information the value: {value}'})
