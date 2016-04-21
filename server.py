from flask import Flask,render_template,request,redirect,abort,send_from_directory
from flask.ext.login import LoginManager,login_user,logout_user,login_required,current_user
from passlib.hash import pbkdf2_sha256

from model import Model
from forms import SignupForm,SigninForm,MakeGroupForm,MakeEventForm,AddUserForm,SimpleVoteForm

import sys

production = "production" in sys.argv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///avalanche.db"

app.config['DEBUG'] = not production
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
    form = MakeEventForm()
    form2 = AddUserForm()
    group = app_model.Group.query.filter_by(id=index).first()
    if group==None or not group.has_user(current_user) :
        abort(404)
    return render_template("group.html",group=group,form=form,form2=form2)

@login_required
@app.route("/vote/<int:index>/<remainder>",methods=["GET","POST"])
def vote(index,remainder):
    event = app_model.Event.query.filter_by(id=index).first()
    method = event.get_method()
    return method.handle_page(remainder,request,current_user.get_membership(event.group))

@login_required
@app.route("/event/<int:index>",methods=["GET"])
def event(index):
    """    # http://stackoverflow.com/a/522578/2033574
    raw_locations = [
        "Tom and Jerry's",
        "McDonald's",
        "China Buffet",
        "Taco Bell",
        "Long John Silver's",
        "AppleBee's",
        "Chili's",
        "Valentinos",
        "Upstream Brewery"
    ]

    form = SimpleVoteForm()
    # form2 = AddUserForm()"""

    event = app_model.Event.query.filter_by(id=index).first()
    
    # winnerVotes = 0
    # winner = -1
    """voteCount = [0]*len(raw_locations) # voteCount[loc_id] == num of votes for that location
    for vote in event.votes:
        loc_id = int(vote.data)
        voteCount[loc_id] += 1
        # if (voteCount[loc_id] > winnerVotes):
            # winnerVotes = voteCount[loc_id]
            # winner = loc_id

    # http://www.tutorialspoint.com/python/list_max.htm
    # http://stackoverflow.com/questions/6193498/pythonic-way-to-find-maximum-value-and-its-index-in-a-list
    winnerVotes = max(voteCount)
    winners = [True if votes == winnerVotes else False for votes in voteCount]

    # print "The winner is: ", winner
    print "The winners are: ", winners

    print voteCount
    locations = [{
        "loc_id": loc_id,
        "name": name,
        "votes": voteCount[loc_id],
        "isWinner": winners[loc_id]
    } for loc_id, name in enumerate(raw_locations)]

    membership = app_model.Membership.query.filter_by(user=current_user,group=event.group).first()
    # print "MEMBERID: ", membership.id
    # event = app_model.Group.query.filter_by(id=index).first()
    # if event==None or not event.has_user(current_user) :
        # abort(404)
        """
    return render_template("event.html",event=event)#,form=form,membership=membership,
#                           locations=locations) # chicken dinner!

@login_required
@app.route("/addvote/<int:event_id>/<int:membership_id>",methods=["POST"])
def addvote(event_id, membership_id):
    form = SimpleVoteForm()
    if form.validate_on_submit():
        # group = app_model.Group.query.filter_by(id=groupIndex).first()
        vote = app_model.Vote(request.form["locationid"])
        event = app_model.Event.query.filter_by(id=event_id).first()
        membership = app_model.Membership.query.filter_by(id=membership_id).first()

        vote.event = event;
        vote.membership = membership;
        # membership = app_model.Membership(current_user,group)
        # app_db.session.add(membership)
        app_db.session.add(event)
        # print(membership.user)
        app_db.session.commit()
        return redirect("/event/{}".format(event_id))

@login_required
@app.route("/setadmin",methods=["GET"])
def setadmin():
    group = app_model.Group.query.filter_by(id=request.args["group"]).first()
    user = app_model.User.query.filter_by(id=request.args["user"]).first()
    admin = current_user.get_membership(group)
    if user != None and group != None and admin != None and admin.is_admin :
        membership = user.get_membership(group)
        membership.is_admin = request.args["is_admin"] == "true"
        app_db.session.commit()
    return redirect("/group/{}".format(request.args["group"]))

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
        membership.is_admin = True
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
        if group is None or user is None or not group.has_user(current_user) or group.has_user(user):
            abort(500)
        app_db.session.add(app_model.Membership(user,group))
        app_db.session.commit()
    return redirect("/group/{}".format(index))

@login_required
@app.route("/addevent/<int:groupIndex>",methods=["POST"])
def addevent(groupIndex):
    form = MakeEventForm()
    if form.validate_on_submit():
        group = app_model.Group.query.filter_by(id=groupIndex).first()
        event = app_model.Event(request.form["eventname"],form.method.data)
        event.group = group;
        # membership = app_model.Membership(current_user,group)
        # app_db.session.add(membership)
        app_db.session.add(event)
        # print(membership.user)
        app_db.session.commit()
        return redirect("/group/{}".format(groupIndex))

@app.route("/static/<remainder>",methods=["GET"])
def get_static(remainder):
    return send_from_directory(app.static_folder,remainder)

if __name__ == "__main__" :
    if production :
        app.run(host="0.0.0.0",port=80)
    else :
        app.run()
