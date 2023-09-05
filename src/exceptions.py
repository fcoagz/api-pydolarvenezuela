from flask import jsonify

def page_not_found(e):
    message = jsonify({"error": "Sorry, the page you were looking for could not be found."})
    message.status_code = 404
    return message

def internal_server_error(e):
    message = jsonify({"error": "Sorry, an internal problem has occurred on the server. Please try again later."})
    message.status_code = 500
    return message
