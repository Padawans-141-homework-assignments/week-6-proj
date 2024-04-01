from flask_smorest import Blueprint

bpusr = Blueprint('usr', 'usr', description='Holds the contents of the users.')

from . import user_res