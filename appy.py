#Import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

#Create engine to connect with database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

app = Flask(__name__)

@app.route("/")
def welcome():
 return (
        f"Welcome to the Hawaii Temps API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>")


@app.route("/api/v1.0/precipitation")
def percipitation():
    
    conn = engine.connect()
    
    query = '''
        SELECT
            date,
            AVG(prcp) as avg_prcp
        FROM
            measurement
        WHERE
            date >= (SELECT DATE(MAX(date), '-1 year') FROM measurement)
        GROUP BY
            date
        ORDER BY
            date
'''

    prcp_df = pd.read_sql(query, conn)

    prcp_df['date'] = pd.to_datetime(prcp_df['date'])

    prcp_df.sort_values('date')

#    prcp_df.set_index('date', inplace = True)
    
    prcp_json = prcp_df.to_json(orient = 'records', date_format = 'iso')
        
    conn.close()
    
    return prcp_json






if __name__ == '__main__':
    app.run(debug=True)