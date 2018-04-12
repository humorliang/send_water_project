from app.__init__ import app
from flask import render_template, redirect, session, url_for, request
from app.models import *
from app.exts import db


@app.route('/')
def index():
    # test = Test(username='zhang')
    # db.session.add(test)
    # db.session.commit()
    # print('-----------')
    return render_template('base.html')
