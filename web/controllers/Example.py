
from flask import Blueprint

route_example = Blueprint('api_example', __name__)

@route_example.route('/', methods=['GET', 'POST'])
def example():
    return 'example'
    