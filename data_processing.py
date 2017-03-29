import csv
from models import *
from app import db
from sqlalchemy import *
import logging as log
import folium


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

# This will return the folium map for a single selected language.
def create_single_map(lang_name):

    threat_level = {

        "Vulnerable" : 'beige',
        "Definitely endangered" : "green",
        "Severely endangered" : "orange",
        "Critically endangered" : 'red',
        "Extinct" : 'black'

    }

    language_map = folium.Map(location=[40,-120], zoom_start = 2) # Zoom out to include world, TODO try narrowing in on selection.


    query = Language.query.filter_by(name = lang_name).all()

    for lang in query:

        lat = lang.latitude
        lon = lang.longitude

        marker_text = '%s originated in %s, it has %s speakers and a threat level of %s. Description: %s' % (lang.name, lang.origin, lang.speakers, lang.threat_level, lang.description)

        color = threat_level[lang.threat_level]

        marker = folium.Marker([lat, lon], popup = marker_text, icon = folium.Icon(color = color))

        marker.add_to(language_map)


    return language_map.save('maps/language_result.html')

def return_all_languages():

    threat_level = {

        "Vulnerable" : 'green',
        "Definitely endangered" : "beige",
        "Severely endangered" : "orange",
        "Critically endangered" : 'red',
        "Extinct" : 'black'

    }

    language_map = folium.Map(location=[40,-120], zoom_start = 2) # Zoom out to include world, TODO try narrowing in on selection.


    query = Language.query.all()

    for lang in query:

        lat = lang.latitude
        lon = lang.longitude

        marker_text = '%s originated in %s, it has %s speakers and a threat level of %s. Description: %s' % (lang.name, lang.origin, lang.speakers, lang.threat_level, lang.description)

        color = threat_level[lang.threat_level]

        marker = folium.Marker([lat, lon], popup = marker_text, icon = folium.Icon(color = color))

        marker.add_to(language_map)


    return language_map.save('maps/all_languages_result.html')


def get_threat_level_map(threat):

    threat_level = {

        "Vulnerable" : 'green',
        "Definitely endangered" : "beige",
        "Severely endangered" : "orange",
        "Critically endangered" : 'red',
        "Extinct" : 'black'

    }


    language_map = folium.Map(location=[40,-120], zoom_start = 2)


    query = Language.query.filter_by(threat_level = threat).all()

    for lang in query:

        lat = lang.latitude
        lon = lang.longitude

        marker_text = '%s originated in %s, it has %s speakers and a threat level of %s. Description: %s' % (lang.name, lang.origin, lang.speakers, lang.threat_level, lang.description)

        color = threat_level[lang.threat_level]

        marker = folium.Marker([lat, lon], popup = marker_text, icon = folium.Icon(color = color))

        marker.add_to(language_map)


    return language_map.save('maps/threat_level_result.html')
