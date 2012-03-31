#! /usr/bin/env python2.7

import sqlite3 as db
import os.path

def create_db(name, path):
    '''Creates a SQLite3 database at the specified location(path) with the
    specified name
    '''

    c = db.connect(os.path.join(path, name))

    c.execute('''CREATE TABLE user(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nick TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT
            )''')

    c.execute('''CREATE TABLE upload(
                user_id INTEGER NOT NULL,
                filename TEXT,
                timestamp INTEGER,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )''')

    #TODO:create the session table

    c.close()

if __name__ == "__main__":
    create_db('upload.db', os.path.abspath('..'))

