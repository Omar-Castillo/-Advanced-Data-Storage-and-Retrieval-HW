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

@app.route("/api/stations")
def stations():
    '''Return a list of stations in our  data'''
    #Use Pandas `read_sql_query` to load a query statement directly into the DataFrame
    stmt = session.query(Measurement).statement
    measurement_df = pd.read_sql_query(stmt, session.bind)
    list_stations = measurement_df['station'].unique()
    #Need to convert the tuple to a list in order to run jsonify call properly
    final_stations = list(np.ravel(list_stations))
 
    return jsonify(final_stations)

@app.route("/api/temperature")
def temperature():
    '''Query for the dates and temperature observations from a year from the last data point'''
    #use date from pandas notebook. A year from last point would be 8-23-16, so we use anything after 8-22-16 as our reference point
    year_ago_date = dt.datetime(2016, 8, 22)
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago_date).order_by(Measurement.date).all()
    # #create an empty list to be filled with info from for loop
    last_year_temp = []
    for date, temp in temp_results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = temp
        last_year_temp.append(temp_dict)
    return jsonify(last_year_temp)

if __name__ == "__main__":
    app.run(debug=True)   