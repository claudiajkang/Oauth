import time
from app import app, db
from werkzeug.security import gen_salt
from app.model.auth import OAuth2Client
from app.util.helpers import current_user, split_by_crlf
from flask import session, request, redirect, render_template


@app.route('/logout')
def logout():
    del session['id']
    return redirect('/')


@app.route('/create_client', methods=('GET', 'POST'))
def create_client():
    user = current_user()

    if not user:
        return redirect('/')

    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''

    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()

    return redirect('/')
