from flask import Flask,render_template,request,redirect,abort,send_from_directory
from flask.ext.login import LoginManager,login_user,logout_user,login_required,current_user
from passlib.hash import pbkdf2_sha256

from model import Model
from forms import SignupForm,SigninForm,MakeGroupForm,AddUserForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///avalanche.db"

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# change this for production
app.secret_key = "Secret"

app.static_folder = "static"

app_model = Model(app)
app_db = app_model.db

login_manager = LoginManager()
login_manager.init_app(app)

# this block defines the method used to retrieve user objects from the database
# for use by the login_manager
@login_manager.user_loader
def user_loader(userid):
    users = app_model.User.query.filter_by(username=userid)
    return users.first() # returns first matching user of None if there is no match

def create_user(username,email,password):
    user = app_model.User(username,email)
    user.password = pbkdf2_sha256.encrypt(password)
    app_db.session.add(user)
    app_db.session.commit()
    return user

# the @app.route decorator is a syntactic sugar that can be a bit tricky.
# @app refers to the app object created at the top with "app = Flask(__name__)"

# app.route is passed arguments describing the contditions under which the associated
# function will execute. in this case, the function responds to requests for "/", the root
# of the server. The return of the function "root" is given to the browser in response
# to requests for "/"
@app.route("/")
def root():
    return render_template("root.html")

@app.route("/hello_world")
def hello():
    return "HELLO WORLD"

@login_required
@app.route("/secret")
def secret():
    return "SECRET"

@login_required
@app.route("/logout",methods=["GET","POST"])
def logout():
    logout_user()
    return redirect("/")

@app.route("/signup",methods=["GET","POST"])
def signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template("signup.html",form=form,signup_errors=[])
    elif request.method == "POST":
        errors=[]
        if form.validate_on_submit():
            if request.form["password"]==request.form["repeat_password"] :
                user = create_user(request.form["username"],request.form["email"],request.form["password"])
                user.authenticated = True
                app_db.session.commit()
                login_user(user)
                return redirect("/")
            else :
                errors.append("Passwords did not match")
        else:
            errors.append("Some fields were empty")
        return render_template("signup.html",form=form,signup_errors=errors)

@app.route("/login",methods=["GET","POST"])
def login():
    print(request.form)
    form = SigninForm()
    if request.method == "GET" :
        return render_template("login.html",form=form,signin_errors=[])
    elif request.method == "POST" :
        if form.validate_on_submit():
            user = app_model.User.query.filter_by(username=request.form["username"]).first()
            if user != None :
                if pbkdf2_sha256.verify(request.form["password"],user.password) :
                    user.authenticated = True
                    app_db.session.commit()
                    login_user(user)
                    return redirect("/")
        return render_template("login.html",form=form,signin_errors=["Incorrect username or password"])

@login_required
@app.route("/group/<int:index>",methods=["GET"])
def group(index):
    form = AddUserForm()
    group = app_model.Group.query.filter_by(id=index).first()
    if group==None or not group.has_user(current_user) :
        abort(404)
    return render_template("group.html",group=group,form=form)

@login_required
@app.route("/mygroups",methods=["GET"])
def mygroups():
    form = MakeGroupForm()
    return render_template("mygroups.html",form = form)

@login_required
@app.route("/addgroup",methods=["POST"])
def addgroup():
    form = MakeGroupForm()
    if form.validate_on_submit():
        group = app_model.Group(request.form["groupname"])
        membership = app_model.Membership(current_user,group)
        app_db.session.add(membership)
        app_db.session.add(group)
        print(membership.user)
        app_db.session.commit()
        return redirect("/mygroups")

@login_required
@app.route("/adduser/<int:index>",methods=["POST"])
def adduser(index):
    form = AddUserForm()
    if form.validate_on_submit():
        group = app_model.Group.query.filter_by(id=index).first()
        user = app_model.User.query.filter_by(username=request.form["username"]).first()
        if group is None or user is None or not group.has_user(current_user) :
            abort(500)
        app_db.session.add(app_model.Membership(user,group))
        app_db.session.commit()
    return redirect("/group/{}".format(index))

@app.route("/static/<remainder>",methods=["GET"])
def get_static(remainder):
    return send_from_directory(app.static_folder,remainder)

if __name__ == "__main__" :
    app.run()
