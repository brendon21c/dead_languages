from app import db


class Language(db.Model):
    """Takes the formatted language information from "language_data.csv" and stores in a database for
    easy access."""


    __tablename__ = "languages"

    id = db.Column('LanguageID', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    origin = db.Column(db.String(50))
    threat_level = db.Column(db.String(50))
    speakers = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.String(100))


    def __init__(self, name, origin, threat, speakers, lat, lon, desc):

        self.name = name
        self.origin = origin
        self.threat_level = threat
        self.speakers = speakers
        self.latitude = lat
        self.longitude = lon
        self.description = desc
