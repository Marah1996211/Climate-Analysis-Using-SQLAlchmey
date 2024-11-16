# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite///:hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

first_five = session.query(measurement.prcp, measurement.date).all()

session.close

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/<start>
    /api/v1.0/<start>/<end>
    '''


    @app.route('/api/v1.0/precipitation')
def precipitation():
    # Query to retrieve the last 12 months of data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)


    @app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.name).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

    @app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()
    tobs_list = [temp[0] for temp in results]
    return jsonify(tobs_list)


    @app.route('/api/v1.0/<start>')
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)