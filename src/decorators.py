from functools import wraps
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker
from .data.engine import engine
from .data.services import is_user_valid
from .core import limiter
from .consts import TOKEN_SECRET

session = sessionmaker(bind=engine)()

def token_required_admin(f):
    """
    Token de autenticación requerido para acceder a las rutas Admin.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if token != TOKEN_SECRET:
            return jsonify({"error": "Token inválido."}), 401
        
        return f(*args, **kwargs)
    return decorated

def token_required_user(f):
    """
    Token de autenticación requerido para acceder a las rutas User.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Requiere token para acceder'}), 401
        if not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401
        return f(*args, **kwargs)
    return decorated

def token_optional_user(f):
    """
    Token de autenticación opcional.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            limiter.limit("100 per hour")(lambda: None)()
            return f(*args, **kwargs)

        if token and not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401
        return f(*args, **kwargs)
    return decorated