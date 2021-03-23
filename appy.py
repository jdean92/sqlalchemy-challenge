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

@app.route('/api/v1.0/stations')
def station():
    
    conn = engine.connect()
    
    query = '''
        SELECT
            s.station AS station_code,
            s.name AS station_name
        FROM
            measurement m
        INNER JOIN station s
        ON m.station = s.station
        GROUP BY
            s.station,
            s.name
    '''

    active_stations_df = pd.read_sql(query, conn)
    
    active_stations_json = active_stations_df.to_json(orient = 'records')
    
    conn.close()
    
    return active_stations_json
    
@app.route('/api/v1.0/tobs')
def measurement():
    
    conn = engine.connect()
    
    query = '''
        SELECT
            s.station AS station_code,
            s.name AS station_name,
            COUNT(*) AS station_count
        FROM
            measurement m
        INNER JOIN station s
        ON m.station = s.station
        GROUP BY
            s.station,
            s.name
        ORDER BY 
            station_count DESC
    '''
    active_stations_df = pd.read_sql(query, conn)
    active_stations_df.sort_values('station_count', ascending=False, inplace=True)
    most_active_station = active_stations_df['station_code'].values[0]
    
    query = f'''
        SELECT
            tobs
        FROM
            measurement
        WHERE 
            station = '{most_active_station}'
            
            AND
            
            date >= (SELECT DATE(MAX(date), '-1 year') FROM measurement)
    '''
    mas_tobs_df = pd.read_sql(query, conn)
    
    mas_tobs_json = mas_tobs_df.to_json(orient = 'records')
    
    conn.close()
    
    return mas_tobs_json







if __name__ == '__main__':
    app.run(debug=True)