__author__ = 'kathan'

from db.utils import namedtuple_factory

import bcrypt
import sqlite3


def authenticate_user(email, password):
    user = get_user_by_email(email)

    user_password = user.password.encode('utf-8')
    password = password.encode('utf-8')

    if user and bcrypt.hashpw(password, user_password) == user_password:
        return user, True

    return None, False

def get_user_by_email(email):
    user = None

    if not email:
        return user

    try:
        con = sqlite3.connect("hdk-db.db")
        con.row_factory = namedtuple_factory
        cursor = con.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email,))

        user = cursor.fetchone()
    finally:
        if con:
            con.close()
    return user
