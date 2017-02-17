import os
import logging

from flask import Flask, url_for, request, render_template, redirect, flash, session
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route('/index')
def index_page():   # displays the index page
    return '<button>Index Page</button>'


@app.route('/user/<username>')
def show_user_profile(username):    # displays the user profile
    return 'Welcome %s' % username


@app.route('/hello')
@app.route('/hello/<name>')
def hello_world(name=None):      # Simple Hello World
    return render_template('hello.html', name_template=name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %s' % post_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            print('runs')
            flash('Successfully logged in')
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect username and password'
            app.logger.warning("Incorrect username and password for user (%s)"
                               , request.form.get('username'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

def valid_login(username, password):
    if username == password:
        print('True')
        return True
    else:
        print('False')
        return False

if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.secret_key = '\x8c0\x91\xa1\x95 \t\xd2\x82\xd0;\x8e\x98\x0c\x1a+\xe4\x18\xee\xca\x80g\x971'

    #logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.run(host=host, port=port)
