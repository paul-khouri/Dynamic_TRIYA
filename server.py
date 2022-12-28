from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples, run_commit_query
from datetime import datetime
import os

app = Flask(__name__)
db_path = 'dbase/triya_data.sqlite'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route("/log_in")
def log_in():
    return None


@app.route("/log_out")
def log_out():
    return None




@app.route("/")
def index():
    # get news
    sql = "select news_id, title, content, updated_at from news order by updated_at desc"
    result = run_search_query_tuples(sql, (), db_path)
    print(result)
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
            outcome = run_commit_query(sql, values_tuple, db_path)
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
            result = run_search_query_tuples(sql, values_tuple, db_path)
            if result is None:
                e_m = "Oops, we could not find a result"
                return render_template("error_page.html", error_message=e_m)
            # build error page
            return render_template("news_cud.html", news_id=news_id, news=result[0])
    else:
        return "Error on News GET POST"


@app.route("/program")
def program():
    # get programs
    sql = "select program_id, name, subtitle, content, image, coachingfee, boathire, coachingfee+boathire as 'total' from program"
    result = run_search_query_tuples(sql, (), db_path)
    print(result)
    return render_template("programs.html", programs=result)


@app.route("/program_cud/<program_id>", methods=["GET", "POST"])
def program_cud(program_id):
    empty_program = {
        'name': "",
        'subtitle': "",
        'content' : "",
        'coachingfee': "0",
        'boathire': "0"

    }
    if request.method == "POST":
        f = request.form
        # special request for image file
        g = request.files['file']
        if program_id == "0":
            sql = "insert into program(name, subtitle, content, coachingfee, boathire, image)" \
                  " values(?,?,?,?,?,? )"
            values_tuple = (f['name'], f['subtitle'], f['content'], f['coachingfee'], f['boathire'],'placeholder.png')
            outcome = run_commit_query(sql, values_tuple, db_path)
        else:
            sql = "update program set name=?, subtitle=?, content=?, coachingfee=?, boathire=? where program_id = ?"
            values_tuple = (f['name'], f['subtitle'], f['content'], f['coachingfee'], f['boathire'], program_id)
            outcome = run_commit_query(sql, values_tuple, db_path)
            if g.filename != "":
                if g.content_type in ["image/jpeg", "image/png"]:
                    g.save(os.path.join(app.config['UPLOAD_FOLDER'], g.filename))
                    size = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], g.filename)).st_size
                    print(size)
                    sql = "update program set image = ? where program_id = ?"
                    values_tuple = (g.filename,program_id)
                    outcome = run_commit_query(sql, values_tuple, db_path)
        if outcome is not None:
            return render_template("error_page.html", error_message=outcome)
        else:
            return redirect(url_for('program'))
    elif request.method == "GET":
        if program_id == "0":
            return render_template("program_cud.html", id=program_id, form_data=empty_program)
        else:
            sql = "select name, subtitle, content, coachingfee, boathire, image from program where program_id=?"
            values_tuple = (program_id,)
            result = run_search_query_tuples(sql, values_tuple, db_path)
            if result is None:
                e_m = "Oops, we could not find a result"
                return render_template("error_page.html", error_message=e_m)
            else:
                return render_template("program_cud.html", id=program_id, form_data=result[0])


@app.route("/event")
def event():
    sql = "select event_id, title, content, event_date from event order by event_date desc"
    result = run_search_query_tuples(sql, (), db_path)
    return render_template("events.html", events=result)


@app.route("/event_cud/<event_id>", methods=["GET", "POST"])
def event_cud(event_id):
    empty_event = {
        'title': "Racing event",
        'content': "Bring your boat",
        'event_date': '2022-12-07T16:12'
    }
    if request.method == "POST":
        f = request.form
        sqlite_date = f['Event Date'].replace("T", " ")+":00"
        if event_id == "0":
            sql = "insert into event(title, content, event_date) values(?,?,?)"
            values_tuple = (f['title'], f['content'], sqlite_date)
            outcome = run_commit_query(sql, values_tuple, db_path)
        else:
            sql = "update event set title=? , content=?, event_date=?  where event_id=?"
            values_tuple = (f['title'], f['content'], sqlite_date, event_id)
            outcome = run_commit_query(sql, values_tuple, db_path)
        if outcome is not None:
            return render_template("error_page.html", error_message=outcome)
        else:
            return redirect(url_for('event'))
    elif request.method == "GET":
        if event_id == "0":
            return render_template("event_cud.html", event=empty_event, event_id=event_id)
        else:
            sql = "select title, content, event_date from event where event_id = ?"
            values_tuple = (event_id,)
            result = run_search_query_tuples(sql, values_tuple, db_path)
            if result is None:
                e_m = "Oops, we could not find a result"
                return render_template("error_page.html", error_message=e_m)
            return render_template("event_cud.html", event_id=event_id, event=result[0])


@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    description = request.args
    print(description.keys())
    expected_keys = ['id', 'table', 'title']
    for k in expected_keys:
        if k not in description.keys():
            return render_template("error_page.html",
                                   error_message="Do not have the required information to delete the item")
    if request.method == "POST":
        id_name = description['table']+"_id"
        sql = "delete from {} where {}=?".format(description['table'], id_name)
        values_tuple = (description['id'],)
        outcome = run_commit_query(sql, values_tuple, db_path)
        if outcome is not None:
            e_m = "Oops, it looks like something went wrong and the post was not deleted"
            return render_template("error_page.html", error_message=e_m)
        else:
            if description['table'] == "event":
                return redirect(url_for('event'))
            elif description['table'] == "program":
                return redirect(url_for('program'))
            else:
                return redirect(url_for('index'))
    elif request.method == "GET":
        return render_template("delete.html", id=description['id'],
                               table=description['table'],
                               delete_message=description['title'])


if __name__ == "__main__":
    app.run(debug=True)
