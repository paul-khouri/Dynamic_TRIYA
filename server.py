from flask import Flask, render_template
from db_functions import run_search_query

app=Flask(__name__)
db_path = 'dbase/triya_data.sqlite'


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