#Import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

#Create engine to connect with database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link)  to the DB
session = Session(engine)



