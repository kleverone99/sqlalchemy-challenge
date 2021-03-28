import numpy as np
import pandas as pd

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

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_prior = '2016-08-23'

# Perform a query to retrieve the data and precipitation scores
    precip_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_prior).\
        order_by(measurement.date).all()
    
    session.close()

    precip_df = pd.DataFrame(precip_data, columns =['date', 'prcp']).set_index('date')

    precip_dict = precip_df.to_dict()

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Perform a query to retrieve stations
    stations = session.query(station.station, station.name).all()
    
    session.close()

    station_df = pd.DataFrame(stations, columns =['station', 'name']).set_index('station')

    station_dict = station_df.to_dict()

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_prior = '2016-08-23'

# Perform a query to retrieve the data and precipitation scores
    temp_data = session.query(measurement.date, measurement.tobs).filter(measurement.station=="USC00519281").filter(measurement.date >= year_prior).all()
    df_temp = pd.DataFrame(temp_data, columns =['date', 'temp']).set_index('date')
    
    session.close()

    tobs_dict = df_temp.to_dict()

    return jsonify(tobs_dict)


if __name__ == '__main__':
    app.run(debug=True)
