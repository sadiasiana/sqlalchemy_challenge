import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station 


app = Flask(__name__) 

@app.route("/")
def home():
    return """<h1><center>Climate App</center></h1><br/>
        <h3><center>/api/v1.0/precipitation</h3></center><br/>
        <h3><center>/api/v1.0/stations</h3></center><br/>
        <h3><center>/api/v1.0/tobs</h3></center><br/>
        <h3><center>/api/v1.0/&lt;start&gt;</h3></center><br/>
        <h3><center>/api/v1.0/&lt;start&gt;/&lt;end&gt;</h3></center>"""

@app.route("/api/v1.0/precipitation") 
def precipitation():
    session = Session(engine)
    sel = [Measurement.date, Measurement.prcp]
    result = session.query(*sel).all()
    session.close()

    precipitation = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation) 


@app.route("/api/v1.0/stations")
def stations(): 
    stations_all = session.query(Station.station, Station.name).all()
    station_list = list(stations_all)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    tobs_data_list = list(tobs_data)
    return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        
        start_day_list = list(start_day)
        
        return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        
        start_end_day_list = list(start_end_day)
        
        return jsonify(start_end_day_list)


if __name__ == "__main__":
    app.run(debug = True)