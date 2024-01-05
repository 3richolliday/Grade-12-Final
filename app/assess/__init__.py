from flask import Blueprint

bp = Blueprint('assess', __name__)

from app.assess import routes