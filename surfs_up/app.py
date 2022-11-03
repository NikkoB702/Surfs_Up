
# Import dependacies.

import pandas as pd
import numpy as np
import datetime as dt

# Import dependacies for SQLAlchemy.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependacies for Flask.

from flask import Flask, jsonify

# Create database.

engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect databases into classes.

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database.

session = Session(engine)

# Create Flask.

app = Flask(__name__)

# Create welcome route.

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create route for Precipitation analysis.

@app.route('/api/v1.0/precipitation')

# Create precipitation function.

def precipitation():

    # Add code that calculates date from one year ago from most recent date in database.

    prev_year= dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)

    # Query through database to get date and precipitation for previous year.

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Create dictionary with date as key and precipitation as value in key:value pair.

    precip = {date: prcp for date, prcp in precipitation}

    # Format the results.

    return jsonify(precip)

# Create route for Stations route

@app.route('/api/v1.0/stations')

# Create stations function
def stations():

    # Query to get all the station names
    results = session.query(Station.station).all()

    # Unravel and convert results to a list
    stations = list(np.ravel(results))

    # Format json to display stations as a dictionary key:value pair
    return jsonify(stations=stations)

# Create route for Temperature route

@app.route('/api/v1.0/tobs')

# Create stations function

def temp_monthly():

    #Add code that calculates date from one year ago from most recent date in database

    prev_year= dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)

    # Query the primary station for all the tobs (temperature observations) from previous year

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    # Unravel results into a 1dimensional array
    temps = list(np.ravel(results))

    # Format json to display stations as a dictionary key:value pair
    return jsonify(temps=temps)

# Create route for Statistics 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create function called stats and add 'start' and 'end' parameters. For now set both to 'None'
def stats(start=None, end=None):

    #Query to select minimum, average and maximum temps from database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Create 'If-Not' statement to determine start and end date
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        # Unravel results into a 1dimensional array
        temps = list(np.ravel(results))

        # Format json to display stations as a dictionary key:value pair
        return jsonify(temps)

    # Query to calculate temp min, max and average with the start dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)