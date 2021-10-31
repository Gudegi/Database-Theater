from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('movies', __name__, url_prefix='/movies')

#영화 목록 페이지
@bp.route('/')
def list():
    return render_template('client_templates/movies-list.html')

#영화 목록 페이지에서 영화 이름 누르면 해당 영화 detail 페이지 랜더링, 각 영화의 이미지, 이름 등 db에 있는 정보들을 인자로 넘겨서 랜더링
'''
@bp.route('/detail/<여기에 db 영화테이블 id 참조>')
def detail(영화테이블.id):
    디비에서 영화 이름등 정보 갖고오고, 
    이미지도 갖고오고
    return render_template('client_templates/movie-info-sidebar-right.html', 인자1, 인자2, 인자3,..)
    '''