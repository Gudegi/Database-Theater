from flask import Blueprint, request, jsonify, make_response
from datetime import datetime, timedelta
from werkzeug.utils import redirect
#from flex.models import Theater, Screenschedule, Movie, Seat, Screen


from rivescript import RiveScript
import re, os

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/', methods=['POST'])
def response():
    query = request.get_json().get("query")

    bot = RiveScript(utf8=True)
    bot.unicode_puctuation = re.compile(r'[.,!?;:]')
    #bot.load_directory("./eg/brain")
    bot.load_directory(os.path.join(os.path.dirname(__file__), "..", "static", "client_static", "chatbot_static", "brain"))
    bot.sort_replies()

    reply = bot.reply("localuesr", query)

    message = {"response": reply}
    #res = make_response(message)
    res = jsonify(message)
    return res