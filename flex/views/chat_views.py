from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from flex.models import Theater, Screenschedule, Movie, Seat, Screen
from sqlalchemy import and_

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/', methods=['POST', 'GET'])
def chat2():
    text = request.get_json().get("query")
    print(text)
    message = {"response": text}
    print(message)
    return jsonify(message)