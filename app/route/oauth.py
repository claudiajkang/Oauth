from app import app
from app.model.user import User
from authlib.oauth2 import OAuth2Error
from app.util.helpers import current_user
from app.oauth2 import authorization, require_oauth
from authlib.integrations.flask_oauth2 import current_token
from flask import request, url_for, render_template, redirect, jsonify


@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()

    if not user:
        return redirect(url_for('home', next=request.url))

    if request.method == "GET":
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None

    return authorization.create_authorization_response(grant_user=grant_user)


@app.route('/oauth/token', methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@app.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@app.route('/api/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)
