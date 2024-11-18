import numpy as np
import datetime as dt  # Add this import

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")  # Fixed database URL (three slashes)

# Reflect an existing database into a new model
base = automap_base()  # Use lowercase `base`
# Reflect the tables
base.prepare(autoload_with=engine)  # Fixed method name to `base.prepare`

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
        f'Welcome to my homepage<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/&lt;start&gt;<br/>'
        f'/api/v1.0/temp/&lt;start&gt;/&lt;end&gt;<br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Query to retrieve the last 12 months of data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()
    session.close()
    precipitation_dict = {date: prcp for date, prcp in prcp}
    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station).all()
    session.close()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list=stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= last_year).all()
    session.close()
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list=tobs_list)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    results = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    
    if not end:
        start = dt.datetime.strptime(start, '%m%d%Y')
        results1 = session.query(*results).filter(measurement.date >= start).all()
        session.close()
        results1_list = list(np.ravel(results1))
        return jsonify(results1_list=results1_list)
    
    # Calculate when we have a start and end date:
    start = dt.datetime.strptime(start, '%m%d%Y')
    end = dt.datetime.strptime(end, '%m%d%Y')
    results_start = session.query(*results).filter(measurement.date >= start, measurement.date <= end).all()
    session.close()
    results_start_list = list(np.ravel(results_start))
    return jsonify(results_start=results_start_list)


if __name__ == '__main__':  # Fixed the typo here: `if__name__` to `if __name__`
    app.run(debug=True)