from flask import Blueprint

bp = Blueprint('sales', __name__)

from app.routes.sales import routes
