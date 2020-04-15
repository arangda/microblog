from flask import Blueprint

bp = Blueprint('shares',__name__)

from app.shares import routes