# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hello")
@app.route("/hello/<name>")
def hello_world(name=None):
    return render_template('hello.html', name=name)

@app.route("/about/")
def about():
    return "About"

@app.route("/projects")
def projects():
    return "Projects"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
