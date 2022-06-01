from functools import wraps
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
import flask_restx
from app import db, api
from datetime import datetime

from flask import Blueprint, request, jsonify
from app.model import User
import sys


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = User.decode_token(request.cookies.get("auth"))
        _user: User = User.current()
        if not _user:
            flask_restx.abort(HTTPStatus.FORBIDDEN, token.get("message"))
        return f(*args, **kwargs)

    return wrapper


from app.routes.user import user_name_space
from app.routes.note import note_name_space

api.add_namespace(user_name_space)
api.add_namespace(note_name_space)
