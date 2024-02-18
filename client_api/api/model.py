import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

database_dir = os.path.join('api')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id          = db.Column(db.Integer, primary_key=True)
    measure     = db.Column(db.String(6), nullable=False)
    time        = db.Column(db.String(6), nullable=False)
    uncertainty = db.Column(db.String(6), nullable=False)

class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id", "measure", "time", "uncertainty")

sensor_schema  = SensorSchema()
sensors_schema = SensorSchema(many=True)
