from http import HTTPStatus
from flask_restx import Resource
from app import api
from app.routes import login_required
from app.routes.note.functions import (
    create_note,
    delete_note,
    fetch_user_notes,
    get_note,
    update_note,
)
from app.routes.note.schemas import (
    note_parser,
    notes_response_schema,
    note_response_schema,
)
from app.utils import general_parser, general_response_schema

note_name_space = api.namespace("note", "Notes Endpoints")


@note_name_space.route("/")
class NoteResource(Resource):
    method_decorators = [login_required]

    @note_name_space.expect(general_parser)
    @note_name_space.marshal_with(notes_response_schema, code=HTTPStatus.OK)
    def get(self):
        data = general_parser.parse_args()
        return fetch_user_notes(
            data.get("page"),
            data.get("per_page"),
        )

    @note_name_space.expect(note_parser)
    @note_name_space.marshal_with(note_response_schema, code=HTTPStatus.CREATED)
    def post(self):
        data = note_parser.parse_args(strict=True)
        return create_note(
            data.get("title"),
            data.get("content"),
        )


@note_name_space.route("/<int:note_id>")
class RUDNoteResource(Resource):
    method_decorators = [login_required]

    @note_name_space.marshal_with(note_response_schema, code=HTTPStatus.OK)
    def get(self, note_id):
        return get_note(note_id)

    @note_name_space.expect(note_parser)
    @note_name_space.marshal_with(notes_response_schema, code=HTTPStatus.OK)
    def put(self, note_id):
        data = note_parser.parse_args()
        return update_note(
            note_id,
            data.get("title"),
            data.get("content"),
        )

    @note_name_space.marshal_with(general_response_schema, code=HTTPStatus.OK)
    def delete(self, note_id):
        return delete_note(
            note_id,
        )
