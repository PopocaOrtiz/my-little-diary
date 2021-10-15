from typing import Union
from flask import render_template, flash, redirect, Response, url_for

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index() -> str:
    return 'Hello, World!'


@app.route('/login', methods=['GET','POST'])
def login() -> Union[str, Response]:
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)