from flask.ext.sqlalchemy import SQLAlchemy

# This file defines the database structure.

class Model():
    def __init__(self,app) :
        self.db = SQLAlchemy(app)
        db = self.db # place db in additional location for clarity

        class User(db.Model):
            id = db.Column(db.Integer,primary_key=True)
            username = db.Column(db.String(80),unique=True)
            email = db.Column(db.String(120),unique=True)
            password = db.Column(db.String())
            authenticated = db.Column(db.Boolean())
            def __init__(self,username,email):
                self.username = username
                self.email = email

            def is_authenticated(self):
                return self.authenticated

            def is_active(self):
                return self.is_authenticated()

            def is_anonymous(self):
                return False
 
            def get_id(self):
                return self.username
        self.User = User
