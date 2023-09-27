from flask import (Blueprint, render_template, request, redirect)
from core.db import get_db

bp = Blueprint('url_shortener', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        db = get_db()
        db.execute('INSERT INTO url (url, clicked) VALUES (?, ?)', (url, 0))
        db.commit()
        return redirect('/')
    else:
        db = get_db()
        urls = db.execute('SELECT url, clicked FROM url').fetchall()
        if urls[0] is not None:
            print(urls[0])
        return render_template('url_shortener/index.html', urls=urls)
