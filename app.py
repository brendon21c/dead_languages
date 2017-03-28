from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exists, and_
import itertools
from datetime import *
import logging as log



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dead_languages_db.sqlite3'
app.config['SECRET_KEY'] = "spoken"

db = SQLAlchemy(app)
from data_processing import *
from models import * # Needs to be after db, otherwise no tables are created.



@app.route('/', methods = ['GET','POST'])
def home_page():

    setup() # inserts into database the first time the program is run. May need to run twice to get to work.


    return render_template("home_page.html", name_list = Language.query.all())


# Check to see if the database is empty, if it is run setup, else break.
def setup():

    query = Language.query.all()

    if not query:

        process_inital_data() # process original csv file.

        write_to_database() # add data I want into database.




if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
