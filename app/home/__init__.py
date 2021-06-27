# app/home/__init__.py

from flask import Blueprint

home = Blueprint('home', __name__)

from app.home import views
