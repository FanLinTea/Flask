#coding:utf8
from . import main
from flask import render_template


@main.route('/')
def Home():
    '''首页'''
    return render_template('Home.html')