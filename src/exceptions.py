from flask import jsonify

def forbidden(e):
    message = jsonify({"error": "El servidor entendió la solicitud, pero se niega a autorizarla."})
    message.status_code = 403
    return message

def page_not_found(e):
    message = jsonify({"error": "No se pudo encontrar la página que estaba buscando."})
    message.status_code = 404
    return message

def internal_server_error(e):
    message = jsonify({"error": "Ha ocurrido un problema interno en el servidor. Por favor, inténtelo de nuevo más tarde."})
    message.status_code = 500
    return message

def gateway_timeout(e):
    message = jsonify({"error": "El servidor estaba actuando como una puerta de enlace o proxy y no recibió una respuesta a tiempo del servidor aguas arriba."})
    message.status_code = 504
    return message