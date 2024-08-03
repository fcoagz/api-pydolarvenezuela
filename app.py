import logging 
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from src.core import limiter
from src.consts import TIMEOUT, GETLOGS
from src import cron
from src.routes import index, monitors, admin
from src.exceptions import (
    forbidden,
    page_not_found,
    internal_server_error,
    gateway_timeout
)

if GETLOGS:
    logging.basicConfig(filename='logs.log', level=logging.INFO)

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(cron.job, 'interval', minutes=TIMEOUT)
scheduler.start()

# app
app = Flask(__name__)
CORS(app)
limiter.init_app(app)
swagger = Swagger(app, template_file='src/swagger.yaml')

# error handling
app.register_error_handler(403, forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(504, gateway_timeout)

# routes
app.register_blueprint(index.route)
app.register_blueprint(monitors.route)
app.register_blueprint(admin.route)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    scheduler.shutdown()