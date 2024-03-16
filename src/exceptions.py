from flask import jsonify

def forbidden(e):
    message = jsonify({"error": "El servidor entendió la solicitud, pero se niega a autorizarla."}), 403
    return message

def page_not_found(e):
    message = jsonify({"error": "No se pudo encontrar la página que estaba buscando. Por favor, consulta la documentación en: https://github.com/fcoagz/api-pydolarvenezuela"}), 404
    return message

def internal_server_error(e):
    message = jsonify({"error": "Ha ocurrido un problema interno en el servidor. Por favor, inténtelo de nuevo más tarde."}), 500
    return message

def gateway_timeout(e):
    message = jsonify({"error": "El servidor estaba actuando como una puerta de enlace o proxy y no recibió una respuesta a tiempo del servidor aguas arriba."}), 504
    return message