from flask.ext.sqlalchemy import SQLAlchemy

# This file defines the database structure.

class Model():
    def __init__(self,app) :
        self.db = SQLAlchemy(app)
        db = self.db # place db in additional location for clarity

        class Membership(db.Model):
            __tablename__ = "memberships"

            id = db.Column(db.Integer,primary_key=True)
            user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
            group_id = db.Column(db.Integer,db.ForeignKey("groups.id"))

            user = db.relationship("User",back_populates="memberships")
            group = db.relationship("Group",back_populates="memberships")
            votes = db.relationship("Vote",back_populates="membership")
            is_admin = db.Column(db.Boolean)

            def __init__(self,user,group):
                self.user = user
                self.group = group
        self.Membership = Membership

        class User(db.Model):
            __tablename__ = "users"

            id = db.Column(db.Integer,primary_key=True)
            username = db.Column(db.String(80),unique=True)
            email = db.Column(db.String(120),unique=True)
            password = db.Column(db.String())
            authenticated = db.Column(db.Boolean())

            memberships = db.relationship("Membership",back_populates="user")

            def __init__(self,username,email):
                self.username = username
                self.email = email
                self.anonymous = False

            def is_authenticated(self):
                return self.authenticated

            def is_active(self):
                return self.is_authenticated()
 
            def get_id(self):
                return self.username

            def has_group(self,group):
                for membership in self.user :
                    if membership.group == group :
                        return True
                return False
        self.User = User
        
        class Group(db.Model):
            __tablename__ = "groups"

            id = db.Column(db.Integer,primary_key=True)
            name = db.Column(db.String(120))
            memberships = db.relationship("Membership",back_populates="group")
            events = db.relationship("Event",back_populates="group")

            def __init__(self,name):
                self.name = name

            def has_user(self,user):
                for membership in self.memberships :
                    if user == membership.user :
                        return True
                return False
        self.Group = Group

        class Event(db.Model):
            __tablename__ = "events"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(120))
            location = db.Column(db.String(120))
            time = db.Column(db.DateTime())
            group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
            group = db.relationship("Group",back_populates="events")
            votes = db.relationship("Vote",back_populates="event")

            def __init__(self,name):
                self.name = name
            
        self.Event = Event

        class Vote(db.Model):
            __tablename__ = "votes"
            id = db.Column(db.Integer, primary_key=True)
            data = db.Column(db.String(120))
            event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
            membership_id = db.Column(db.Integer, db.ForeignKey("memberships.id"))

            event = db.relationship("Event",back_populates="votes")
            membership = db.relationship("Membership",back_populates="votes")

            def __init__(self,data):
                self.data = data
            
        self.Vote = Vote
