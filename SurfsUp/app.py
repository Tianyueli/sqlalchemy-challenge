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

engine = create_engine("sqlite:///Data_Visualization_BootCamp/Assignments/Module_10_Assignment/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
hawaii_measurement = Base.classes.measurement
hawaii_station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
session.query(hawaii_measurement)
session.query(hawaii_station)

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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )



@app.route("/api/v1.0/precipitation")
def precipitation():
    ls_12_mths = dt.date(2017,8,23) - dt.timedelta(days=365)
    ls_yr_prcp = session.query(hawaii_measurement.date, hawaii_measurement.prcp).\
    filter(hawaii_measurement.date >= ls_12_mths).all()

    session.close()

def date():

    session.close()

@app.route("/api/v1.0/tobs")

def prcp():
    session.close()

# @app.route("/api/v1.0/<start>")
# def 
# session.close()

# @app.route("/api/v1.0/<start>/<end>")

# session.close()
    
if __name__ == "__main__":
    app.run(debug=True)