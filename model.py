from flask.ext.sqlalchemy import SQLAlchemy

# This file defines the database structure.

class Model():
    def __init__(self,app) :
        self.db = SQLAlchemy(app)
        db = self.db # place db in additional location for clarity

        class GroupMembership(db.Model):
            __tablename__ = "group_memberships"

            id = db.Column(db.Integer,primary_key=True)
            user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
            group_id = db.Column(db.Integer,db.ForeignKey("groups.id"))
        self.GroupMembership = GroupMembership

        class User(db.Model):
            __tablename__ = "users"

            id = db.Column(db.Integer,primary_key=True)
            username = db.Column(db.String(80),unique=True)
            email = db.Column(db.String(120),unique=True)
            password = db.Column(db.String())
            authenticated = db.Column(db.Boolean())
            groups = db.relationship("Group",secondary="group_memberships",backref="users")

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
        self.User = User
        
        class Group(db.Model):
            __tablename__ = "groups"

            id = db.Column(db.Integer,primary_key=True)
            name = db.Column(db.String(120))
            def __init__(self,name):
                self.name = name
        self.Group = Group
