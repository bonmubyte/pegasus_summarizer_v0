from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../summarizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True


db = SQLAlchemy(app)

# Import routes at the end to avoid circular imports
from yourapp import routes

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()
