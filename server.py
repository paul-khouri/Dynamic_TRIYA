from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples

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
    return render_template("index.html", page_data=result)

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

def get_programs(p):
    sql = "select name, subtitle, description, coachingfee, boathire, coachingfee+boathire as 'total', image from program;"
    result = run_search_query(sql,p)
    return result


if __name__ == "__main__":
    app.run(debug=True)