from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

def jwt_middleware():
    if request.method == 'OPTIONS':
        return '', 200
    
    if 'Authorization' in request.headers:
        try:
            token = request.headers['Authorization'].split()[1]
            identity = get_jwt_identity()
        except Exception as e:
            return { "message": str(e) }, 401
    else:
        return { "message": "Missing Authorization Header" }, 401