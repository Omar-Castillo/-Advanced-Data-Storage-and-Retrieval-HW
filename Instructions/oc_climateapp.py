###
#Flask Routes for Surf's Up Homework
###
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# import pandas and datetime
import pandas as pd 
import datetime as dt
#import flask
from flask import Flask, jsonify

#create engine for database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

#Create our session(link) from Python to the DB
session = Session(engine)

#Create an app, being sure to pass __name__
app = Flask(__name__)

#Define API Home Page

@app.route("/")
def home():
    return( """Welcome to the Home page for Omar Castillo's Surf's Up API!<br/>
            The routes that are API routes that will be available are the following:<br/>
            /api/precipitation<br/>
            /api/stations<br/>
            /api/temperature<br/>
            /api/'start' and /api/'start'/'end'"""
    )
   
@app.route("/api/precipitation")
def precipitation():
    '''Return a list of precipitation data including date, precipitation'''
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. Using in dates from 8/23/2016
    #filter out none values
    #sorted by measurement date
    year_ago_date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.date,Measurement.prcp)\
        .filter(Measurement.date > year_ago_date,Measurement.prcp != "None").order_by(Measurement.date).all()
    #Create a dictionary from raw precipitation data
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

if __name__ == "__main__":
    app.run(debug=True)   