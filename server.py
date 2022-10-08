from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples, run_commit_query

app=Flask(__name__)
db_path = 'dbase/triya_data.sqlite'
app.secret_key= "tempkey"


@app.template_filter()
def currency_format(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.route("/")
def index():
    result = get_page_one(db_path)
    news = get_all_news(db_path)
    return render_template("index.html", page_data=result, news_data= news)

@app.route('/update_delete_newsitem/<post_id>', methods=['GET','POST'])
def update_delete_newsitem(post_id):
    if request.method == "GET":
        if session and session["Authorisation"]==0:

            if post_id == "0":
                null_data={
                    "id":0,
                    "header":"",
                    "details":"",
                    "content":""
                }
                return render_template("update_delete_newsitem.html", p_id=post_id, post_data= null_data)
            else:
                result= get_single_news(db_path, post_id)
                print(result[0])
                session["delete"]={"id":post_id,"table": "newsitem" }

                #id, header, details, content
                return render_template("update_delete_newsitem.html", p_id = post_id, post_data= result[0])
        else:
            return "<h1>Not Logged In</h1>".format(post_id)
    elif request.method == "POST":
        f=request.form
        if f["id"] == "0":
            sql = "insert into newsitem(header, details, content, updated_at) values(?,?,?, datetime('now'));"
            values_tuple=(f['header'], f['details'], f['content'])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('index'))
        else:
            return "<h1> Form Action Post_ID = {}</h1>".format(post_id)

@app.route("/delete_item")
def delete_item():
    if session["delete"]["table"]=="newsitem":
        sql = "delete from newsitem where id = ?"
        values_tuple = (session["delete"]["id"])
        run_commit_query(sql, values_tuple, db_path)
    return redirect(url_for('index'))

@app.route("/programs")
def programs():
    result = get_programs(db_path)
    return render_template("programs.html", page_data=result)

@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/log-in", methods=["GET","POST"])
def log_in():
    if request.method == "GET":
        return render_template("log-in.html")
    elif request.method == "POST":
        f= request.form
        # look for user in dbase
        sql = "select password, authorisation from member where username = ?"
        values_tuple = (f["User Name"],)
        result = run_search_query_tuples(sql,values_tuple,db_path)
        pwd = f["Password"]

        if result is None:
            return render_template("log-in.html", error="Your details are not recognised")
        elif pwd != result[0]["password"]:
            return render_template("log-in.html", error="Your details do not match")
        else:
            session["Username"]=f["User Name"]
            session["Authorisation"] = result[0]["authorisation"]
            return redirect(url_for('index'))


@app.route("/log-out", methods=["GET","POST"])
def log_out():
    session.clear()
    return redirect(request.referrer)


def get_page_one(p):
    sql="select header, content, image from page where pagenumber = 1;"
    result = run_search_query(sql,p)
    return result

def get_all_news(p):
    sql="select id, header, details, content from newsitem order by updated_at desc;"
    result = run_search_query(sql,p)
    return result

def get_single_news(p, id):
    sql="select id, header, details, content from newsitem where id = ?;"
    values_tuple= (id,)
    result = run_search_query_tuples(sql,values_tuple, p)
    return result


def insert_newsitem():
    return None

def update_newsitem():
    return None

def delete_newsitem():
    return None

def get_programs(p):
    sql = "select name, subtitle, description, coachingfee, boathire, coachingfee+boathire as 'total', image from program;"
    result = run_search_query(sql,p)
    return result


if __name__ == "__main__":
    app.run(debug=True)