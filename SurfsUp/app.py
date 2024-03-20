# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Data_Visualization_BootCamp/Assignments/Module_10_Assignment/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
hawaii_measurement = Base.classes.measurement
hawaii_station = Base.classes.station
ls_12_mths = dt.date(2017,8,23) - dt.timedelta(days=365)
# Create our session (link) from Python to the DB
# session = Session(engine)
# session.query(hawaii_measurement)
# session.query(hawaii_station)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        F"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    ls_yr_prcp = session.query(hawaii_measurement.date, hawaii_measurement.prcp).\
    filter(hawaii_measurement.date >= ls_12_mths).all()
    precipitation_list = []
    for date,prcp in ls_yr_prcp:
        precipitation_dict = {"date":date, "precipitation":prcp}
        precipitation_list.append(precipitation_dict)
    session.close()
    
    return jsonify(precipitation_list)
  
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_data = session.query(hawaii_station.station, hawaii_station.name).all()
    station_ls = []
    for station, name in station_data:
        station_dict = {"station":station, "name": name}
        station_ls.append(station_dict)
    session.close()
    return jsonify(station_ls)


@app.route("/api/v1.0/tobs")
def date():
    session = Session(engine)
    most_active_station_temp = session.query(hawaii_measurement.date, hawaii_measurement.tobs).\
    filter(hawaii_measurement.station == 'USC00519281', hawaii_measurement.date >= ls_12_mths).\
    all()
    temp_list = []
    for date,temp in most_active_station_temp:
        temp_dict = {"date":date, "temperature":temp}
        temp_list.append(temp_dict)
    session.close()
    
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    # start = dt.date(2017,10,23)
    # start_stat_list = []
    session = Session(engine)
    tob_stats = session.query(func.min(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs)).\
    filter(hawaii_measurement.date >= start).\
    all()
    # min = session.query(func.min(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()
    # max = session.query(func.max(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()
    # avg = session.query(func.avg(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()

    min, avg, max = tob_stats[0]
    stat_dict ={"TMIN":min,"TAVG":avg, "TMAX":max}
        # start_stat_list.append(stat_dict)
    session.close()
    return jsonify(stat_dict)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    session = Session(engine)
    # start = dt.date(2017,8,23)
    # end = dt.date(2017,10,23)
    # end_stat_list = []
    session = Session(engine)
    tob_stats = session.query(func.min(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs)).\
    filter(hawaii_measurement.date >= start).\
    filter(hawaii_measurement.date < end).\
    all()

    # min = session.query(func.min(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()
    # max = session.query(func.max(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()
    # avg = session.query(func.avg(hawaii_measurement.tobs)).filter(hawaii_measurement.date >= start).all()

    min, avg, max = tob_stats[0]
    stat_dict_end ={"TMIN":min,"TAVG":avg, "TMAX":max}
    session.close()
    return jsonify(stat_dict_end)
    
if __name__ == "__main__":
    app.run(debug=True)