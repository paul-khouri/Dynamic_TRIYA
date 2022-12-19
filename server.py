from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples, run_commit_query
import os

app = Flask(__name__)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/programs")
def programs():
    return render_template("programs.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/information")
def information():
    return render_template("information.html")


if __name__ == "__main__":
    app.run(debug=True)
