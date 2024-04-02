from flask_smorest import Blueprint

bplog = Blueprint('signup', 'signup', description = 'Controls logging in and out.')

from . import loginandout