from flask import jsonify

def page_not_found(e):
    return jsonify({"error": "Sorry, the page you were looking for could not be found."}), 404

def internal_server_error(e):
    return jsonify({"error": "Sorry, an internal problem has occurred on the server. Please try again later."}), 500
