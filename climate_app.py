import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# last 12 months variable
last_date = '2016-08-23'
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
#link from python to DB
    session = Session(engine)
#precipitation scores query
    p_scores = session.query(measurement.date, measurement.prcp).\
                filter(measurement.date >= last_date).\
                order_by(measurement.date).all()
    return jsonify(p_scores)

@app.route("/api/v1.0/stations")
def stations():
    #link from python to DB
    session = Session(engine)
    stations_info = session.query(Station.station, Station.name).all()
    return jsonify(stations_info)

@app.route("/api/v1.0/tobs")
def tobs():
    #link from python to DB
    session = Session(engine)
    tobs_results = session.query(measurement.date, measurement.station, measurement.tobs).\
                filter(measurement.date >= last_date).all()
    return jsonify(tobs_results)

if __name__ == '__main__':
    app.run(debug=True)
