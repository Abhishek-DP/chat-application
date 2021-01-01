from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()
 
class chat_registration(db.Model):
    __tablename__ = 'user_registration'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False,unique=True)
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=db.func.now(), nullable=False)
 
    def __init__(self, email,name,password):
        self.email = email
        self.name = name
        self.password = password
 
    def __repr__(self):
        return f"{self.email}:{self.name}"

    