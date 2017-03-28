import csv
from models import *
from app import db
from sqlalchemy import *
import logging as log


def process_inital_data():

    language_data = []

    # I needed to encodeing because I was getting an UTC error. I got this from stackoverflow.
    with open('data.csv', 'r', encoding='ISO-8859-1') as csvfile:

        reader = csv.reader(csvfile)

        columns = reader.__next__()

        for row in reader:

            name = row[1]
            origin = row[4]
            threat = row[7]
            speakers = row[10]
            lat = float(row[12])
            lon = float(row[13])
            desc = row[14]

            language_data.append([name,origin,threat,speakers,lat,lon,desc])


    with open('language_data.csv', 'w') as csvfile:

        writer = csv.writer(csvfile, quoting = csv.QUOTE_NONNUMERIC)
        writer.writerow(['name', 'origin', 'threat', 'speakers', 'lat', 'lon', 'desc'])
        writer.writerows(language_data)

def write_to_database():

    with open('language_data.csv', 'r') as csvfile:

        reader = csv.reader(csvfile)

        columns = reader.__next__()

        for row in reader:

            name = row[0]
            origin = row[1]
            threat = row[2]
            speakers = row[3]
            lat = row[4]
            lon = row[5]
            desc = row[6]

            language_entry = Language(name,origin,threat,speakers,lat,lon,desc)

            db.session.add(language_entry)
            db.session.commit()
