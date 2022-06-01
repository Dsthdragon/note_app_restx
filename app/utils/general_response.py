from flask_restx import fields
from app import api

general_response_schema = api.model(
    "General Response",
    {
        "status": fields.String,
        "message": fields.String,
    },
)

general_list_response_schema = api.inherit(
    "General List Response",
    general_response_schema,
    {
        "has_next": fields.Boolean,
        "per_page": fields.Integer,
        "total": fields.Integer,
    },
)
