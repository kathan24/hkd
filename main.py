__author__ = 'kathan'

from flask import Flask, render_template, redirect, request, session, flash, url_for
from utils.decorators import login_required
from db import user
import os

app = Flask(__name__)


# changing jinja options so that it does not clash with Angularjs
jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
    cache_size=0
))
app.jinja_options = jinja_options


@app.route("/", methods=['GET'])
@login_required
def home():
    user_first_name = session.get("user_first_name")
    user_last_name = session.get("user_last_name")
    return render_template("index.html", first_name=user_first_name, last_name=user_last_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if all([email, password]):
            user_obj, authenticated = user.authenticate_user(email, password)
            if authenticated:
                session['logged_in'] = True
                session['user_first_name'] = user_obj.firstName
                session['user_last_name'] = user_obj.lastName

    return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    flash('Logged out', 'success')
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, threaded=True, use_reloader=False, host='127.0.0.1', port=8051)