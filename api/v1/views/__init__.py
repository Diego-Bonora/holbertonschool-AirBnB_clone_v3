#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('simple_page', __name__, url_prefix='/api/v1')

from api.v1.views.amenities import *  # nopep8
from api.v1.views.cities import *  # nopep8
from api.v1.views.index import *  # nopep8
from api.v1.views.states import *  # nopep8
from api.v1.views.users import *  # nopep8
from api.v1.views.places_reviews import *  # nopep8
