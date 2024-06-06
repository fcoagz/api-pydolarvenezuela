from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from src.routes import index, monitors
from src.exceptions import (
    forbidden,
    page_not_found,
    internal_server_error,
    gateway_timeout
)

app = Flask(__name__)
swagger = Swagger(app, template_file='src/swagger.yaml')
CORS(app)

# error handling
app.register_error_handler(403, forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(504, gateway_timeout)

# routes
app.register_blueprint(index.route)
app.register_blueprint(monitors.route)