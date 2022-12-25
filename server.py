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
    sql = "select news_id, title, content, updated_at from news order by updated_at desc"
    result = run_search_query_tuples(sql, (), db_path)
    return render_template("index.html", news=result)


@app.route("/news_cud/<news_id>", methods=["GET", "POST"])
def news_cud(news_id):
    dummy_news = {
        'title': "One more sailor needed",
        'content': "We have room for one more college age sailor to join us for the Winter program. "
                   "We need an even number of sailors for the double handed 420 yacht.If you are keen, "
                   "lets know.Got to http://www.triya.co.nz/.../fleet-racing-sailing-development"
                   "Cheers Phil"
    }
    empty_news = {
        'title': "",
        'content': ""
    }
    if request.method == "POST":
        f = request.form
        # a new post
        if news_id == "0":
            sql = "insert into news (title, content, updated_at) values(?,?, datetime('now'))"
            values_tuple = (f['title'], f['content'])
            outcome = run_commit_query(sql,values_tuple, db_path)
        else:
            # update current post
            sql = "update news set title=? , content=?, updated_at=datetime('now') where news_id=?"
            values_tuple = (f['title'], f['content'], news_id)
            outcome = run_commit_query(sql, values_tuple, db_path)
        if outcome is not None:
            return render_template("error_page.html", error_message=outcome)
        else:
            return redirect(url_for('index'))
    elif request.method == "GET":
        if news_id == "0":
            # render form with empty data
            return render_template("news_cud.html", news_id=news_id, news=dummy_news)
        else:
            # render form with data using news_id
            # run query again to get the news item
            sql = "select title, content, updated_at from news where news_id = ?"
            values_tuple = (news_id,)
            result = run_search_query_tuples(sql, values_tuple,db_path)
            if result is None:
                e_m = "Oops, we could not find a result"
                return render_template("error_page.html", error_message=e_m)
            # build error page
            return render_template("news_cud.html", news_id=news_id, news=result[0])
    else:
        return "Error on News GET POST"


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


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        description = request.args
        print(description.keys())
        expected_keys = ['id', 'table', 'title']
        have_keys = True
        for k in expected_keys:
            if k not in description.keys():
                have_keys = False
                return render_template("error_page.html",
                                       error_message="Do not have the required information to delete the item")
        return render_template("delete.html", id =description['id'],
                               table=description['table'],
                               delete_message=description['title'] )







if __name__ == "__main__":
    app.run(debug=True)
