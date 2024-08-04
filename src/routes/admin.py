from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from ..consts import TOKEN_SECRET
from ..data.engine import engine
from ..data.services import (
    create_user as create_user_,
    modificate_user as modificate_user_,
    delete_user as delete_user_,
    get_users as get_users_
)

route   = Blueprint('admin', __name__)
session = sessionmaker(bind=engine)()

@route.get('/api/admin/get_users')
def get_users_route():
    token_admin = request.headers.get('Authorization')
    
    if token_admin != TOKEN_SECRET:
        return jsonify({"error": "Token inválido."}), 401
    
    users = get_users_(session)
    return jsonify(users), 200

@route.post('/api/admin/create_user')
def create_user():
    token_admin = request.headers.get('Authorization')
    name = request.form.get('name')
    
    if token_admin != TOKEN_SECRET:
        return jsonify({"error": "Token inválido."}), 401
    
    if name:
        try:
            token = create_user_(session, name)
            return jsonify({"message": "Usuario creado exitosamente.", "token": token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    return jsonify({"error": "Faltan datos."}), 400

@route.put('/api/admin/modificate_user')
def modificate_user():
    token_admin = request.headers.get('Authorization')
    id = request.form.get('id')
    is_premium = request.form.get('is_premium')
    
    if token_admin != TOKEN_SECRET:
        return jsonify({"error": "Token inválido."}), 401
    
    if all([id, is_premium]):
        modificate_user_(session, id, is_premium)
        return jsonify({"message": "Usuario modificado exitosamente."}), 200
    
    return jsonify({"error": "Faltan datos."}), 400

@route.delete('/api/admin/delete_user')
def delete_user():
    token_admin = request.headers.get('Authorization')
    id = request.form.get('id')
    
    if token_admin != TOKEN_SECRET:
        return jsonify({"error": "Token inválido."}), 401
    
    if id:
        delete_user_(session, id)
        return jsonify({"message": "Usuario eliminado exitosamente."}), 200
    
    return jsonify({"error": "Faltan datos."}), 400