from flask import Blueprint

route = Blueprint('index', __name__)

@route.get('/')
def index():
    return "<p>Welcome to the Dolar Venezuela API. Go to documentation: <a href='https://github.com/fcoagz/api-pydolarvenezuela'>https://github.com/fcoagz/api-pydolarvenezuela</a></p>"