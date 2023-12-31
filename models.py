from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
  

    username = db.Column(db.Text,  
                   nullable=False, unique=True) #restrict to 20 characters

    password = db.Column(db.Text, 
                         nullable=False, 
                         unique=False)

    email = db.Column(db.Text, 
                         nullable=False) #restrict to 50 characters
    
    first_name = db.Column(db.Text, nullable=False)# restrict to no longer than 30 chars

    last_name = db.Column(db.Text, nullable=False) #restrict to no longer than 30 chars

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name) 
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        #if u (checking if u even exists)
        if user and bcrypt.check_password_hash(user.password, pwd):  
            #u.password in the db checked against the pwd entered.
            #bcrypt.check_password_hash is built in to bcrypt
            # return user instance
            return user
        else:
            return False
        
class Feedback(db.Model):
     """Feedback."""

     __tablename__ = "feedback"
        
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     content = db.Column(db.Text, nullable=False)
     username = db.Column(
            db.String(20),
            db.ForeignKey('users.username'),
            nullable=False,
        )
