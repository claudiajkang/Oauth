from flask import session
from app.model.user import UserModel


def current_user():
    if 'id' in session:
        uid = session['id']
        return UserModel.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]
