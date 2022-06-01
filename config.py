import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI")
        or "mysql+pymysql://root:" "@localhost/note_app?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    SECRET_KEY = "12345678"
    ERROR_404_HELP = False

    SUCCESS_STATUS = "success"
    ERROR_STATUS = "error"
