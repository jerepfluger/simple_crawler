from flask import Blueprint

routes = Blueprint('routes', __name__)

from .straight_crawler_controller import *
from .differed_crawler_controller import *
