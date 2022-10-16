from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query, run_search_query_tuples, run_commit_query
import os

app=Flask(__name__)
db_path = 'dbase/triya_data.sqlite'
app.secret_key= "tempkey"

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.template_filter()
def currency_format(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.route("/")
def index():
    sql = "select header, content, image from page where pagenumber = 1;"
    result = run_search_query(sql, db_path)
    sql="select id, header, details, content from newsitem order by updated_at desc;"
    news = run_search_query(sql,db_path)
    return render_template("index.html", page_data=result, news_data= news)


@app.route('/update_delete_newsitem/<id>', methods=['GET','POST'])
def update_delete_newsitem(id):
    null_data = {
        "id": 0,
        "header": "",
        "details": "",
        "content": ""
    }
    # arriving at page through link
    if request.method == "GET":
        # check authorisation
        if session and session["Authorisation"]==0:
            # should check post_id is digit ?
            if id == "0":
                # have arrived from new post link
                #use null data package for the form values
                return render_template("update_delete_newsitem.html", id=id, post_data= null_data)
            else:
                # get the required post
                sql = "select id, header, details, content from newsitem where id = ?;"
                values_tuple = (id,)
                result = run_search_query_tuples(sql, values_tuple, db_path)
                # only want the first item so use result[0]
                # set up deletion data if required
                session["delete"]={"id":id,"table": "newsitem" }
                # run template with form fields filled with post data
                return render_template("update_delete_newsitem.html", id = id, post_data= result[0])
        else:
            # if authorisation failed go to error page
            return render_template("error.html")
    elif request.method == "POST":
        f=request.form
        if f["id"] == "0":
            # create a new news item
            sql = "insert into newsitem(header, details, content, updated_at) values(?,?,?, datetime('now'));"
            values_tuple=(f['header'], f['details'], f['content'])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('index'))
        else:
            # update news item
            sql="update newsitem set header = ?, details = ?, content = ?, updated_at = datetime('now') where id = ?"
            values_tuple = (f['header'], f['details'], f['content'], f["id"])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('index'))



@app.route("/programs")
def programs():
    sql = "select id, name, subtitle, description, coachingfee, boathire, coachingfee+boathire as 'total', image from program;"
    result = run_search_query(sql,db_path)
    return render_template("programs.html", page_data=result)

@app.route("/aud_program/<id>", methods=['GET','POST'])
def aud_program(id):
    null_data = {
        "id": 0,
        "name": "New Program",
        "subtitle": "Further explanation",
        "description": "More description",
        "coachingfee": 20.00,
        "boathire": 15.00
    }
    if request.method == "GET":
        if session and session["Authorisation"] == 0:
            if id == "0":
                # have arrived from new program link
                # use null data
                return render_template("aud_program.html", id=id, form_data=null_data)
            else:
                # get the required program (could use session variable ?
                sql = """select id, name, subtitle, description, coachingfee, boathire, 
                        coachingfee+boathire as 'total', image from program where id = ?;"""
                values_tuple = (id,)
                result = run_search_query_tuples(sql, values_tuple, db_path)
                print(result)
                # only want the first item so use result[0]
                # set up deletion data if required
                session["delete"] = {"id": id, "table": "program"}
                session['returnpage']=url_for('programs')
                # run template with form fields filled with post data
                return render_template("aud_program.html", id=id, form_data=result[0])
        else:
            # if authorisation failed go to error page
            return render_template("error.html")

    elif request.method == "POST":
        error = None
        f=request.form
        # special request for image file
        g = request.files['file']
        if id == "0":
            # adding a new program
            if g.content_type == "image/jpeg":
                g.save(os.path.join(app.config['UPLOAD_FOLDER'], g.filename))
                size = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], g.filename)).st_size
                print(size)
                sql= "insert into program(name, subtitle, description, coachingfee, boathire, image, updated_at) values(?,?,?,?,?,?, datetime('now'));"
                values_tuple= (f['name'], f['subtitle'], f['description'], f['coachingfee'], f['boathire'], g.filename)
                run_commit_query(sql,values_tuple,db_path)
                return redirect(url_for('programs'))
            else:
                error = "You have not selected an appropriate image"
                print(g.content_type)
                return render_template("aud_program.html", id=id, form_data=f, error=error)
        else:
            # updating a program
            if g.filename == "":
                # update without changing the image
                sql = """ update program set name = ?, subtitle = ?, description = ?, coachingfee = ?, 
                boathire = ?, updated_at = datetime('now') where id = ?"""
                values_tuple= (f['name'], f['subtitle'], f['description'], f['coachingfee'], f['boathire'], id)
                run_commit_query(sql, values_tuple, db_path)
            elif g.content_type == "image/jpeg":
                # update with image change
                sql = """ update program set name = ?, subtitle = ?, description = ?, coachingfee = ?, 
                boathire = ?, image = ?,updated_at = datetime('now') where id = ?"""
                values_tuple= (f['name'], f['subtitle'], f['description'], f['coachingfee'], f['boathire'],g.filename, id)
                run_commit_query(sql, values_tuple, db_path)
            else:
                # image file selected but is not of the right type
                error = "You have not selected an appropriate image, you can leave this blank"
                print(g.content_type)
                return render_template("aud_program.html", id=id, form_data=f, error=error)
            return redirect(url_for('programs'))


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

@app.route("/delete_item")
def delete_item():
    values_tuple = (session["delete"]["id"])
    if session["delete"]["table"]=="newsitem":
        sql = "delete from newsitem where id = ?"
        run_commit_query(sql, values_tuple, db_path)
        session.pop("delete")
        return redirect(url_for('index'))
    elif session["delete"]["table"] =="program":
        sql = "delete from program where id = ?"
        run_commit_query(sql, values_tuple, db_path)
        session.pop("delete")
        return redirect(url_for('programs'))

@app.route("/images")
def images():
    files = []
    for x in os.listdir(app.config['UPLOAD_FOLDER']):
        if x.lower().endswith((".jpg",".png")):
            files.append(x)

    print(files)
    return render_template("images.html", files=files)

def print_image_data(g):
    print(g)
    print(type(g))
    print(g.filename)
    print(g.stream)
    print(g.__dict__.keys())
    print(g.name)
    print(type(g.headers))
    print(g.content_type)


if __name__ == "__main__":
    app.run(debug=True)