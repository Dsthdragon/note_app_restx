from dataclasses_jsonschema import SchemaType
from app import api
from flask_restx import fields, reqparse, inputs
from app.utils import AppRequestParser, general_response_schema
from app.model import User


login_parser = AppRequestParser(bundle_errors=True)
login_parser.add_argument(
    "email",
    required=True,
    help="Email Address is required",
    location="json",
    type=inputs.email(check=True),
)
login_parser.add_argument(
    "password",
    required=True,
    location="json",
    help="Password is required",
    type=str,
)
register_parser = AppRequestParser(bundle_errors=True)
register_parser.add_argument(
    "email",
    required=True,
    help="Email Address is required",
    location="json",
    type=inputs.email(check=True),
)
register_parser.add_argument(
    "first_name",
    required=True,
    location="json",
    help="First Name is required",
    type=str,
)
register_parser.add_argument(
    "password",
    required=True,
    location="json",
    help="Password is required",
    type=str,
)
register_parser.add_argument(
    "last_name",
    required=True,
    location="json",
    help="Last Name is required",
    type=str,
)


user_schema = api.model(
    "User",
    {
        "id": fields.Integer,
        "email": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "created": fields.DateTime(),
        "updated": fields.DateTime(),
    },
)


user_response_schema = api.inherit(
    "User Response ",
    general_response_schema,
    {
        "status": fields.String,
        "message": fields.String,
        "data": fields.Nested(user_schema),
    },
)

users_response_schema = api.inherit(
    "Users Response ",
    general_response_schema,
    {
        "status": fields.String,
        "message": fields.String,
        "data": fields.List(fields.Nested(user_schema, skip_none=True)),
    },
)
# UserSchema: ma.Schema = marshmallow_dataclass.class_schema(User)()
