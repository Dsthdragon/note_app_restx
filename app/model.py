from dataclasses import dataclass
from datetime import timedelta, timezone, datetime
from flask import request
import jwt
from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.types import TypeDecorator
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses_jsonschema import JsonSchemaMixin
from config import Config

from app import db


class DateTimeUTC(TypeDecorator):
    impl = DateTime(timezone=True)
    cache_ok = True
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return value.astimezone(timezone.utc)


@dataclass
class User(db.Model, JsonSchemaMixin):
    id: int = Column(
        Integer,
        primary_key=True,
    )
    created: datetime = db.Column(
        DateTimeUTC(),
        default=func.now(),
    )
    email: str = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )
    first_name: str = db.Column(
        db.String(80),
        nullable=False,
    )
    last_name: str = db.Column(
        db.String(80),
        nullable=False,
    )
    password_hash = Column(
        db.String(500),
        nullable=False,
    )
    updated: datetime = db.Column(
        DateTimeUTC(),
        onupdate=func.now(),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password,
        )

    def generate_token(self, expires):
        return jwt.encode(
            {
                "id": self.id,
                "expires": expires,
                "expiration_date": str(datetime.utcnow() + timedelta(days=1)),
            },
            Config.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            if (
                payload["expires"]
                and datetime.strptime(
                    payload["expiration_date"], "%Y-%m-%d %H:%M:%S.%f"
                )
                < datetime.utcnow()
            ):
                return {"message": "token expired. please log in again."}
            return {
                "id": payload["id"],
            }
        except jwt.ExpiredSignatureError:
            return {"message": "Signature expired. Please log in again."}
        except jwt.InvalidTokenError:
            return {"message": "Invalid token. Please log in again."}

    @staticmethod
    def current() -> "User":
        return User.query.get(User.decode_token(request.cookies.get("auth")).get("id"))


class Note(db.Model, JsonSchemaMixin):
    id: int = Column(
        Integer,
        primary_key=True,
    )
    title: str = db.Column(
        String(200),
        nullable=False,
    )
    content: str = db.Column(
        Text,
        nullable=False,
    )

    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user: "User" = db.relationship(
        "User",
        backref=db.backref("notes", lazy=True),
    )
    created: datetime = db.Column(
        DateTimeUTC(),
        default=func.now(),
    )
    updated: datetime = db.Column(
        DateTimeUTC(),
        onupdate=func.now(),
    )
