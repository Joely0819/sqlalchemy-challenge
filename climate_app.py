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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

#HomePage: List all available routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start/end<br/>"
    )


#Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
#link from python to DB
    session = Session(engine)
#precipitation scores query
    p_scores = [measurement.date, measurement.prcp]
    query_result = session.query(*p_scores).all()
    session.close()

    precipitation = []
    for date, prcp in query_result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)


#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
#stations query
    stations_info = [Station.station, Station.name]
    query_result = session.query(*stations_info).all()
    session.close()

    stations = []
    for station, name in query_result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name 
        stations.append(station_dict)
    return jsonify(stations)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_results = [measurement.station, measurement.tobs]
    query_result = session.query(*tobs_results).filter(measurement.date >=  '2016-08-23').all()
    session.close()

    tobs_active = []
    for date, tobs in query_result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature Observation Data"] = tobs
        tobs_active.append(tobs_dict)
    return jsonify(tobs_active)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    session.close()

    tobs_start = []
    for min,avg,max in query_result:
        tobs_start_dict = {}
        tobs_start_dict["Min"] = min
        tobs_start_dict["Average"] = avg
        tobs_start_dict["Max"] = max
        tobs_start.append(tobs_start_dict)
    return jsonify(tobs_start)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. 
@app.route("/api/v1.0/<start>/<end>")
def get_start_end(start,end):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    tobs_start_end = []
    for min,avg,max in query_result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_start_end.append(tobs_dict)
    return jsonify(tobs_start_end)


if __name__ == '__main__':
    app.run(debug=True)
