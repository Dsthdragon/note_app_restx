from dataclasses_jsonschema import SchemaType
from app import api
from flask_restx import fields, inputs
from app.utils import (
    AppRequestParser,
    general_response_schema,
    general_list_response_schema,
)
from app.model import User, Note
from app.routes.user.schemas import user_schema

note_parser = AppRequestParser()
note_parser.add_argument(
    "title",
    required=True,
    help="Title is Required",
    location="json",
    type=str,
)
note_parser.add_argument(
    "content",
    required=True,
    help="Content is Required",
    location="json",
    type=str,
)

note_schema = api.model(
    "NoteModel",
    {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String,
        "user_id": fields.Integer,
        "user": fields.Nested(user_schema),
        "created": fields.DateTime(),
        "updated": fields.DateTime(),
    },
)

note_response_schema = api.inherit(
    "NoteResponse ",
    general_response_schema,
    {
        "data": fields.Nested(note_schema, skip_none=True),
    },
)

notes_response_schema = api.inherit(
    "NotesResponse ",
    general_list_response_schema,
    {
        "data": fields.List(fields.Nested(note_schema, skip_none=True)),
    },
)
