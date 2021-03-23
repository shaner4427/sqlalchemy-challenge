import numpy
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///C:\\Users\\shane\\OneDrive\\Desktop\\GitHub\\Repos\\sqlalchemy-challenge\\Resources\\hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurements = Base.classes.measurement
Station = Base.classes.station 

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def main():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation<br/>")
def precipitation():   
    final_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurements.date))).all()
    max_date_string = final_date[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")

    begin_date = max_date - dt.timedelta(365)

    precipitation_data = session.query(func.strftime("%Y-%m-%d", Measurements.date), Measurements.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurements.date) >= begin_date).all()

    results_dict = {}
    for result in precipitation_data:
        results_dict[result[0]] = result[1]

    return jsonify(results_dict)

@app.route("/api/v1.0/stations<br/>")
def stations():
    stations = session.query(Station).all()

    station_list = []
    for station in stations:
        station_dict = {}
        station_dict["station"] = station

    return jsonify(station_list)


