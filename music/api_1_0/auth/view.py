from . import auth
from flask import render_template
# from flask_wtf import

@auth.route('/login')
def login():
    return render_template('loginxxxx.html')