from flask import Flask, render_template, abort, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/rohan/project/rap-ai/TC1Admin/admin.db'
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

admin = Admin(app)


class CustomRules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(30))
    sugession_id = db.Column(db.String(30))


class SecureModelView(ModelView):
    def is_accessible(self):
        if session["logged_in"]:
            return True
        else:
            abort(403)


@app.route("/", methods=["GET", "POST"])
def baseuser():
    if request.method == "POST":
        print(request.form.get("username"))
        print(request.form.get("password"))
        if request.form.get("username") == "admin" and request.form.get("password") == "admin":
            print("CORRECT STUFF")
            session["logged_in"] = True
            return redirect("/admin")
        else:
            print("WRG STUFF")
            return render_template("login.html", falied=True)
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form.get("username"))
        print(request.form.get("password"))
        if request.form.get("username") == "admin" and request.form.get("password") == "admin":
            print("CORRECT STUFF")
            session["logged_in"] = True
            return redirect("/admin")
        else:
            print("WRG STUFF")
            return render_template("login.html", falied=True)
    return render_template("login.html")


@app.route("/sendsession", methods=["POST"])
def sendsession():
    json_value = request.json
    return {"session_id": json_value["session_id"],
    "MSG" : "BUY STUFF"}

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        session["logged_in"] = False
        return redirect("/")


admin.add_view(SecureModelView(CustomRules, db.session))
admin.add_view(LogoutView(name='logout', endpoint='logout'))


if __name__ == '__main__':
    app.run(debug=True)
