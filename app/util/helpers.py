from flask import session
from app.model.user import User


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]
