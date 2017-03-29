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

    threat_level = [

        "Vulnerable",
        "Definitely endangered",
        "Severely endangered",
        "Critically endangered",
        "Extinct"
    ]

    if request.method == 'POST':

        box_check = request.form.get('check')

        if box_check:

            return_all_languages()

            return render_template('results.html', map = '.maps/all_languages_result.html')


        else:

            if request.form['button'] == 'lang_select':


                selection = request.form['lang']
                print(selection)

                create_single_map(selection)

                return render_template('results.html', map = '.maps/language_result.html')

            if request.form['button'] == 'threat_select':

                threat = request.form['threat_form']

                get_threat_level_map(threat)

                return render_template('results.html', map = '.maps/threat_level_result.html')



    return render_template("home_page.html", name_list = Language.query.all(), threat_list = threat_level)

# This is not working
# @app.route('/<path:filename>')
# def show_map(page_name):
#
#     return Flask.send_from_directory(app.maps, page_name)



# Check to see if the database is empty, if it is run setup, else break.
def setup():

    query = Language.query.all()

    if not query:

        process_inital_data() # process original csv file.

        write_to_database() # add data I want into database.

        return redirect(url_for('home_page'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
