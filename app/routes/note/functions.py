from http import HTTPStatus
from flask_restx import abort

from flask import jsonify, make_response
from app.model import User, Note
from config import Config
from app import db


def fetch_user_notes(page=None, per_page=None):
    page = page if page else 0
    per_page = per_page if per_page else Config.POSTS_PER_PAGE
    notes = Note.query.filter_by(user_id=User.current().id)

    notes = notes.paginate(page, per_page, False)
    return (
        dict(
            status=Config.SUCCESS_STATUS,
            message="User Notes Found",
            data=notes.items,
            has_next=notes.has_next,
            per_page=per_page,
            total=notes.total,
        ),
        HTTPStatus.OK,
    )


def create_note(title, content):
    if not title:
        abort(HTTPStatus.BAD_REQUEST, "Title is Required!", status=Config.ERROR_STATUS)
    if not content:
        abort(
            HTTPStatus.BAD_REQUEST, "Content is Required!", status=Config.ERROR_STATUS
        )

    note: Note = Note(title=title, content=content, user_id=User.current().id)
    db.session.add(note)
    db.session.commit()
    return (
        dict(status=Config.SUCCESS_STATUS, message="Note Created", data=note),
        HTTPStatus.CREATED,
    )


def update_note(id, title, content):
    if not title:
        abort(HTTPStatus.BAD_REQUEST, "Title is Required!", status=Config.ERROR_STATUS)
    if not content:
        abort(
            HTTPStatus.BAD_REQUEST, "Content is Required!", status=Config.ERROR_STATUS
        )

    note: Note = Note.query.filter_by(user_id=User.current().id, id=id).first()
    if not note:
        abort(HTTPStatus.NOT_FOUND, "Note not found", status=Config.ERROR_STATUS)

    note.title = title
    note.content = content
    db.session.commit()
    return (
        dict(status=Config.SUCCESS_STATUS, message="Note Updated", data=note),
        HTTPStatus.OK,
    )


def get_note(id):

    note: Note = Note.query.filter_by(user_id=User.current().id, id=id).first()
    if not note:
        abort(HTTPStatus.NOT_FOUND, "Note not found", status=Config.ERROR_STATUS)
    return (
        dict(status=Config.SUCCESS_STATUS, message="Note Found", data=note),
        HTTPStatus.OK,
    )


def delete_note(id):

    note: Note = Note.query.filter_by(user_id=User.current().id, id=id).first()
    if not note:
        abort(HTTPStatus.NOT_FOUND, "Note not found", status=Config.ERROR_STATUS)
    db.session.delete(note)
    db.session.commit()
    return (
        dict(status=Config.SUCCESS_STATUS, message="Note Delete"),
        HTTPStatus.OK,
    )
