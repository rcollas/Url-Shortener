from flask import (Blueprint, render_template, request, redirect)
from core.db import get_db
from hashids import Hashids

bp = Blueprint('url_shortener', __name__)
hashids = Hashids(min_length=4)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        db = get_db()

        if len(url) == 0 or request.host_url in url:
            return redirect('/')

        try:
            db.execute('INSERT INTO url (url, clicked) VALUES (?, ?)', (url, 0))
            db.commit()
        except db.IntegrityError:
            return redirect('/')

        return redirect('/')
    else:
        db = get_db()
        db_urls = db.execute('SELECT id, url, clicked FROM url').fetchall()
        urls = [{'url': f'{request.host_url}{hashids.encode(url["id"])}', 'clicked': url['clicked']} for url in db_urls]
        return render_template('url_shortener/index.html', urls=urls)


@bp.route('/<id>')
def get_route(id):
    url_id = hashids.decode(id)
    db = get_db()
    redirect_url = db.execute('SELECT url, clicked FROM url WHERE id = ?', (url_id)).fetchone()
    if redirect_url and url_id is not None:
        try:
            db.execute('UPDATE url SET clicked = clicked + 1 WHERE id = ?', (url_id))
            db.commit()
        except db.IntegrityError:
            return redirect('/')
        return redirect(redirect_url['url'])
    return redirect('/')
