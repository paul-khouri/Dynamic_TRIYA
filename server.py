from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples, run_commit_query
from datetime import datetime
import os

app = Flask(__name__)
db_path = 'dbase/triya_data.sqlite'


@app.template_filter()
def currency_format(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.template_filter()
def news_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %H:%M")


@app.template_filter()
def event_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y")


@app.template_filter()
def event_time(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%H:%M")


@app.route("/")
def index():
    # get news
    sql = "select title, content, updated_at from news order by updated_at desc"
    result = run_search_query_tuples(sql, (), db_path)
    return render_template("index.html", news=result)


@app.route("/news_cud/<news_id>")
def news_cud(news_id):
    return render_template("news_cud.html")


@app.route("/programs")
def programs():
    # get programs
    sql = "select name, subtitle, content, image, coachingfee, boathire, coachingfee+boathire as 'total' from programs"
    result = run_search_query_tuples(sql, (), db_path)
    return render_template("programs.html", programs=result)


@app.route("/events")
def events():
    sql = "select title, content, event_date from events order by event_date desc"
    result = run_search_query_tuples(sql, (), db_path)
    return render_template("events.html", events=result)


@app.route("/information")
def information():
    return render_template("information.html")


if __name__ == "__main__":
    app.run(debug=True)
