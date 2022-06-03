from http import HTTPStatus
from flask_restx import abort

from flask import jsonify, make_response
from app.model import User
from config import Config
from app import db


def login_user(email, password):

    user: User = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password=password):
        abort(
            HTTPStatus.UNAUTHORIZED,
            "Invalid Login Details",
            status=Config.ERROR_STATUS,
        )

    headers = [
        ("Set-Cookie", f"auth={user.generate_token(True)};path=/;SameSite=None;Secure;")
    ]
    return (
        (
            {
                "status": Config.SUCCESS_STATUS,
                "message": "User Login Successful",
                "data": user,
            },
        ),
        HTTPStatus.ACCEPTED,
        headers,
    )


def login_user_v2(email, password):

    user: User = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password=password):
        abort(
            HTTPStatus.UNAUTHORIZED,
            "Invalid Login Details",
            status=Config.ERROR_STATUS,
        )

    headers = [
        ("Set-Cookie", f"auth={user.generate_token(True)};path=/;SameSite=None;Secure;")
    ]
    return (
        {
            "status": Config.SUCCESS_STATUS,
            "message": "User Login Successful",
            "data": user,
        },
        HTTPStatus.ACCEPTED,
        headers,
    )


def register_user(email, first_name, last_name, password):
    if not first_name:
        abort(
            HTTPStatus.BAD_REQUEST,
            "First name is required",
            status=Config.ERROR_STATUS,
        ), HTTPStatus.ACCEPT
    if not last_name:
        abort(
            HTTPStatus.BAD_REQUEST,
            "Last name is required",
            status=Config.ERROR_STATUS,
        )

    user: User = User.query.filter_by(email=email).first()
    if user:
        abort(
            HTTPStatus.BAD_REQUEST,
            "Email Address is already in system",
            status=Config.ERROR_STATUS,
        )

    user: User = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password=password)
    db.session.add(user)
    db.session.commit()

    return {
        "status": Config.SUCCESS_STATUS,
        "message": "User Account Created",
        "data": user,
    }, HTTPStatus.CREATED


def get_current_user():
    user: User = User.current()
    return {
        "status": Config.SUCCESS_STATUS,
        "message": "User Found",
        "data": user,
    }, HTTPStatus.OK
