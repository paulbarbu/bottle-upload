#! /usr/bin/env python2.7

import bottle
from bottle import run, debug, get, post, request, template, redirect, install, response
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware
import re
import os.path
import sqlite3
import logging

import err
import const

#TODO test this
@get('/')
def index():
    if not is_logged_in():
        redirect('/login')
    else:
        redirect('/upload')

#TODO test this
@get('/register')
def register_view():
    if not is_logged_in():
        return template('register')
    else:
        redirect('/upload')

#TODO test this
@post('/register')
def register_bl(db):
    '''Attempt to create the user if the provided credentials are fine
    If the credentials don't match the criteria then show the user some errors
    '''
    message = None
    error = None

    nick = request.forms.nick.lower()
    email = request.forms.email.lower()
    password = request.forms.password

    state = {
            'nick': nick,
            'email': email
    }

    if is_valid_nick(nick):
        if is_valid_email(email):
            if is_valid_password(password):
                import hashlib

                password = hashlib.sha1(password).hexdigest()

                result = add_user(db, nick, email, password)

                if result is True:
                    message = const.R_SUCCESS
                    logging.info('{0}({1}) has registered'.format(nick, email))
                elif result is False:
                    error = err.DB
                else:
                    error = result
            else:
                error = err.PASS
        else:
            error = err.EMAIL
    else:
        error = err.NICK

    del password

    return template('register', message=message, error=error, state=state)

#TODO test this
@get('/login')
def login_view():
    if not is_logged_in():
        return template('login')
    else:
        redirect('/upload')

#TODO test this
@post('/login')
def login_bl(db):
    import hashlib

    nick = request.forms.nick.lower()
    password = hashlib.sha1(request.forms.password).hexdigest()

    message = {}
    error = None

    uid  = get_user_id(db, nick, password)

    if uid:
        sess = request.environ.get('beaker.session')
        sess['uid'] = uid

        #TODO add expiration time if the user checks "remember me"
        #set the cookie_expires and session.timeout time to 30 days
        #or just overwrite the beaker.session.id cookie writing the same session
        #id but another expiry date, session.timeout stays 30 days
        #else, if remember me wasn't checked, cookie_expires: True, and
        #session.timeout: 1220

        message = const.L_SUCCESS
        nick = get_nick_by_id(db, uid)

        if nick:
            message += ' as ' + nick
            logging.info('{0} has logged in'.format(nick))
        else:
            message += '!'
            logging.info('Someone has logged in')

    elif uid is None:
        error = err.NO_USER
    else:
        error = err.DB

    return template('login', message=message, error=error)

#TODO test this
@get('/upload')
def upload(db):
    if not is_logged_in():
        redirect('/login')
    else:
        sess = request.environ.get('beaker.session')
        sess.get_by_id(request.cookies.get('beaker.session.id'))

        return 'Hello ' + get_nick_by_id(db, sess['uid'])

def is_valid_nick(nick):
    '''A nick is valid when it contains at least one alphanumeric character'''
    if not nick or not re.match('^[a-zA-Z0-9_-]+$', nick):
        return False

    return True

def is_valid_password(password):
    '''A password is valid when it contains at least six characters'''
    if len(password) < 6:
        return False

    return True

def is_valid_email(email):
    '''Validates an email address
    http://code.activestate.com/recipes/65215-e-mail-address-validation/#c6
    '''
    if re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', email):
        return True

    return False

def is_valid_sqlite3(db):
    '''Validates the SQLite3 database file by checking the first bytes
    Check section 1.2.1 Magic Header String of http://www.sqlite.org/fileformat.html
    Note that I'm discarding the last byte, namely: '\0'
    '''

    if not os.path.isfile(db):
        return False

    with open(db, 'r') as f:
        if f.read(15) == 'SQLite format 3':
            return True

        return False

#TODO test this
def add_user(db, nick, email, password):
    '''Add a user to the database and log the action
    Return True is the user was added succesfully, else Fasle
    '''

    try:
        db.execute('INSERT INTO user(nick, email, password) VALUES(?,?,?)',
            (nick, email, password))
    except sqlite3.IntegrityError as e:
        if 'email' in str(e):
            return err.UNIQUE_EMAIL
        elif 'nick' in str(e):
            return err.UNIQUE_NICK
        else:
            logging.exception(e)
            return False
    except Exception as e:
        logging.exception(e)
        return False

    return True

#TODO test this
def get_user_id(db, nick, hashed_pass):
    '''Returns the matching user's ID, else None
    If an unexpected exception is caught False will be returned
    The password passed as argument must be already hashed
    '''

    try:
        cursor = db.execute('SELECT id FROM user WHERE nick=? AND password=?',
                (nick, hashed_pass))
    except Exception as e:
        logging.exception(e)
        return False

    rv = cursor.fetchone()

    if rv is None:
        return None

    return int(rv[0])

#TODO test this
def get_nick_by_id(db, uid):
    '''Get's the user's nickname by his id
    If the user doesn't exists None will be returned and in case of errors False
    will be returned
    '''

    try:
        cursor = db.execute('SELECT nick FROM user WHERE id=?', (uid,))
    except Exception as e:
        logging.exception(e)
        return False

    rv = cursor.fetchone()

    if rv is None:
        return None

    return str(rv[0])

def is_logged_in():
    '''Check whether the user sent a cookie that holds a Beaker created
    session id
    '''

    sess_id = request.cookies.get('beaker.session.id', False)

    if not sess_id:
        return False

    sess = request.environ.get('beaker.session')

    if 'uid' not in sess:
        return False

    return True

install(SQLitePlugin(dbfile=const.DB_FILENAME))

session_opts = {
        'session.auto': True,
        'session.cookie_expires': True,
        'session.timeout': 1440,
        'session.type': 'file',
        'session.data_dir': './data',
        'session.httponly': True,
}

app = bottle.app()
app = SessionMiddleware(app, session_opts)

if __name__ == '__main__':
    logging.basicConfig(filename='logs.log', level=logging.DEBUG,
            format='%(levelname)s: %(asctime)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S')

    if not is_valid_sqlite3(const.DB_FILENAME):
        print err.SQLITE_FILE_USER
        logging.critical(err.SQLITE_FILE)
    else:
        debug(True)
        run(app=app, host="localhost", port="8080", reloader=True)

    #TODO: delete old session files aka logout
    #TODO: add a menu
