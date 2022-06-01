from http import HTTPStatus
from flask_restx import Resource, reqparse
from flask_restx import inputs
from app import api
from app.model import User
from app.routes import login_required
from config import Config
from .functions import get_current_user, login_user, register_user
from .schemas import (
    register_parser,
    user_response_schema,
    users_response_schema,
    login_parser,
)

user_name_space = api.namespace("user", "User Endpoints")


@user_name_space.route("/")
class UserResource(Resource):
    @user_name_space.expect(register_parser)
    @user_name_space.marshal_with(user_response_schema, code=HTTPStatus.CREATED)
    def post(self):
        data = register_parser.parse_args(strict=True)
        return register_user(
            data.get("email"),
            data.get("first_name"),
            data.get("last_name"),
            data.get("password"),
        )

    @user_name_space.marshal_with(user_response_schema, code=HTTPStatus.OK)
    @login_required
    def get(self):
        return get_current_user()


@user_name_space.route("/login")
class UserLoginResource(Resource):
    @user_name_space.marshal_with(user_response_schema, code=HTTPStatus.ACCEPTED)
    @user_name_space.expect(login_parser)
    def post(self):
        data = login_parser.parse_args(strict=True)
        return login_user(
            data.get("email"),
            data.get("password"),
        )
