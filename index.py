#! /usr/bin/env python2.7

from bottle import run, debug, get, post, request, template, redirect
import re

import err

@get('/')
def index():
    if not request.cookies.get('user', False):
        redirect('/login')

@get('/register')
def register_view():
    return template('register')

@post('/register')
def register_bl():
    '''Attempt to create the user if the provided credentials are fine
    If the credentials don't match the criteria then show the user some errors
    '''
    message = None
    error = None

    nick = request.forms.nick
    email = request.forms.email
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
                #add to database
            else:
                error = err.PASS
        else:
            error = err.EMAIL
    else:
        error = err.NICK

    del password

    return template('register', message=message, error=error, state=state)

@get('/login')
def login():
    return template('login')

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

if __name__ == '__main__':
    debug(True)
    run(host="localhost", port="8080", reloader=True)
