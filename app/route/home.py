from app import app, db
from app.model.user import User
from flask import request, session
from app.model.auth import OAuth2Client
from app.util.helpers import current_user
from flask import render_template, redirect


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        session['id'] = user.id
        next_page = request.args.get('next')

        if next_page:
            return redirect(next_page)

        return redirect('/')

    user = current_user()
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)