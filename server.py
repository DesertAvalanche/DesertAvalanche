from flask import Flask,render_template,request,redirect
from flask.ext.login import LoginManager,login_user
from passlib.hash import pbkdf2_sha256

from model import Model
from forms import SignupForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///avalanche.db"

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# change this for production
app.secret_key = "Secret"

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
                errors.append(form.password)
                errors.append(form.repeat_password)
        else:
            errors.append("Some fields were empty")
        return render_template("signup.html",form=form,signup_errors=errors)

if __name__ == "__main__" :
    app.run()
