PASS = {
    'msg': 'Passwords must be longer than six characters!',
    'code': 1
}

NICK = {
    'msg': 'Nicknames must consist of at least one aphanumeric character!',
    'code': 2
}

EMAIL = {
    'msg': "The email provided doesn't appear to be valid!",
    'code': 3
}

DB = {
    'msg': 'An unknown database error has occured, please try again!',
    'code': 4
}

UNIQUE_NICK = {
    'msg': 'Nick already in use, please choose another one!',
    'code': 5
}

UNIQUE_EMAIL = {
    'msg': 'Email already in use!',
    'code': 6
}

NO_USER = {
    'msg': 'The credentials provided are incorrect!',
    'code': 7
}

SQLITE_FILE_USER = '''Aborting: The SQLite DB file is invalid!
Use bin/schema.py to create a valid one!'''

SQLITE_FILE = '''Invalid SQLite database'''

NO_FILE = {
    'msg': 'No file selected!',
    'code':  8
}
