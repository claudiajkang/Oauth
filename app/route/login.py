from app import app
from flask import session, redirect


@app.route('/logout')
def logout():
    del session['id']
    return redirect('/')