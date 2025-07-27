from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from helpers.application import app

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12345@localhost:5432/censoescolar"
db.init_app(app)