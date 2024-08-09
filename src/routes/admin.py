from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from ..decorators import token_required_admin
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
@token_required_admin
def get_users_route():
    users = get_users_(session)
    return jsonify(users), 200

@route.get('/api/admin/reload_monitors')
@token_required_admin
def reload_monitors():
    from ..cron import reload_monitors
    
    reload_monitors()
    return jsonify({"message": "Monitores recargados exitosamente."}), 200

@route.post('/api/admin/create_user')
@token_required_admin
def create_user():
    name = request.form.get('name')
    if name:
        try:
            token = create_user_(session, name)
            return jsonify({"message": "Usuario creado exitosamente.", "token": token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    return jsonify({"error": "Faltan datos."}), 400

@route.put('/api/admin/modificate_user')
@token_required_admin
def modificate_user():
    id = request.form.get('id')
    is_premium = request.form.get('is_premium')

    if all([id, is_premium]):
        modificate_user_(session, id, is_premium)
        return jsonify({"message": "Usuario modificado exitosamente."}), 200
    
    return jsonify({"error": "Faltan datos."}), 400

@route.delete('/api/admin/delete_user')
@token_required_admin
def delete_user():
    id = request.form.get('id')

    if id:
        delete_user_(session, id)
        return jsonify({"message": "Usuario eliminado exitosamente."}), 200
    
    return jsonify({"error": "Faltan datos."}), 400