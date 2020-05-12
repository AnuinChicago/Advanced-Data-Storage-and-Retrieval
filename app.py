import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (start date as 'YYYY-MM-DD')<br/>"
        f"/api/v1.0/<start>/<end> (start date/end date as 'YYYY-MM-DD')"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #last date of data entry
    last_date=session.query(func.max(Measurement.date)).scalar()

    #One year before last data entry
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query date and precipitaion
    results = session.query(Measurement.date, Measurement.prcp).\
    filter( Measurement.date >= query_date).\
    group_by(Measurement.date).all()
    
    session.close()

    # convert list to  dict
    all_prcp =dict(results)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of stations
    results=session.query(Measurement.station).\
    group_by(Measurement.station).all()

    session.close()

    #convert list of tuples to list
    all_stations= list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #last date of data entry
    last_date=session.query(func.max(Measurement.date)).scalar()

    #One year before last data entry
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query( Measurement.tobs  ).\
    filter(Measurement.station == 'USC00519281').\
    filter( Measurement.date >= '2016-08-23').\
    order_by(Measurement.date.desc()).all()

    session.close()

    #convert list of tuples to list
    all_tobs= list(np.ravel(results))
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    session.close()
    
    #convert list of tuples to list
    all_start= list(np.ravel(results))
    
    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()

    session.close()
    
    #convert list of tuples to list
    all_start_end= list(np.ravel(results))
    
    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)
