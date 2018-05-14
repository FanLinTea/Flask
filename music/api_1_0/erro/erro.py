from . import aerro
from flask import render_template

@aerro.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@aerro.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500