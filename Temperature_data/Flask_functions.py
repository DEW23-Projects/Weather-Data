from flask import Flask, render_template, request, redirect, url_for, flash,Response
from Psycopg2_functions import *
from flask import Flask
from Web_projects import getgroup
import datetime
import geocode
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def Home():

    return render_template('home.html')



def list_temps(lat,lon):
    conn= pgconnect()
    cursor = conn.cursor()
    query = f"""SELECT s.station_id From Station s Join
    Temperature t On t.Station_Id = s.Station_Id
    Where t.Quality = 'G'
    order by abs((s.longitude-{lon})*(s.longitude-{lon})+ (s.latitude-{lat})*(s.latitude-{lat})) ASC limit 1;"""
    cursor.execute(query)
    station_id = cursor.fetchone()[0]
    query = f"""SELECT s.Station_Name, t.Value, t.Timestamp From Station s Join
    Temperature t On t.Station_Id = s.Station_Id
    where s.station_id = {station_id}
    Order By t.Timestamp Desc"""
    cursor.execute(query)
    Templist = cursor.fetchall()
    xyList = Templist
    temperatures = [row[1] for row in xyList]
    timestamps = [row[2] for row in xyList]
    print(xyList)
    timestamps = timestamps[::-1]
    print(timestamps)
    for i in range(len(timestamps)):
        print(timestamps[i])
        timestamps[i] = datetime.datetime.fromtimestamp(int(timestamps[i])/1000).strftime('%Y-%m-%d %H')
    station_name = xyList[0][0]
    return temperatures,timestamps,station_name
    
# Here follow temperature data items.
@app.route("/temperature", methods=['GET','POST'])
def temperature():
    return render_template('temperature.html')


@app.route("/get_temperature", methods=['GET','POST'])
def get_temperature():
    if request.method == 'POST':
        location = request.form.get("location")
        x = geocode.getlocation(location)
        
        
        temperatures, timestamps,station_name = list_temps(*x)
        return render_template('temperature.html', temperatures = temperatures, timestamps = timestamps, station_name = station_name)
    else:
        return render_template('temperature.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)