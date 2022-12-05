import requests
import json




url = 'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1.json'
jhandle = requests.get(url)
text= jhandle.text
json_object = json.loads(text)

#"summary":"Data från alla aktiva mätstationer för senaste timmen i en fil."
all_station_href = json_object["stationSet"][0]["link"][0]["href"] 
station_data_json = json.loads(requests.get(all_station_href).text)

# Getting here that the key we want to get for the last hour is "period"
# separate_keys(station_data_json)



# Period href  -- The data we require from the past hour should be located on the href acquired from here.
# href = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour.json"
period_href = station_data_json["period"][0]["link"][0]["href"]
period_data_text = requests.get(period_href).text
period_data_json = json.loads(period_data_text)
# separate_keys(period_data_json)

# We are now referred to another file which is rumored to contain our data.
# Lucky! We finally acquired some useful data from our inquiries. We acquire the first item in the list for examination.
# href = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour/data.json"
hour_href = period_data_json["data"][0]["link"][0]["href"]
hour_data_text = requests.get(hour_href).text
hour_data_json = json.loads(hour_data_text)
""" 
Examination of this print gives us the information:
dict_keys(['key', 'name', 'owner', 'ownerCategory', 'measuringStations', 'from', 'to', 'height', 'latitude', 'longitude', 'value'])
print(hour_data_json["station"][0].keys())
 """

"""
I want to further examine what's in value.
print(hour_data_json["station"][0]["value"])
"""
# The print statement above gives this string:
# [{'date': 1670061600000, 'value': '-5.9', 'quality': 'G'}]
# I'm going to make the assumption that the key "value" is referring to temperature value.
# I have thus found a method for acquiring the temperature value of a given station for the latest hour. 
# 

"""
Let's run through this station, give the temperatures for each station name and print name and temperature.
print("station name:",hour_data_json["station"][0]["name"], ", Temperature: ", hour_data_json["station"][0]["value"][0]["value"])
"""

# We get this information about the key quality in value: 
# Kvalitetskoderna:
# Grön (G) = Kontrollerade och godkända värden.
# Gul (Y) = Misstänkta eller aggregerade värden. Grovt kontrollerade arkivdata och okontrollerade realtidsdata (senaste 2 tim).

# We may want to check only values which are checked and confirmed correct.
# I want to then put the above print-statement into an if-clause.
"""
if hour_data_json["station"][0]["value"][0]["quality"] == "G":
    print("station name:",hour_data_json["station"][0]["name"], ", Temperature: ", hour_data_json["station"][0]["value"][0]["value"])
"""


# With this infomation I should be easily able to reverse-engineer my way back,
# collect links to the json object for each station and print the temperature for each station.
"""
print("station name:",hour_data_json["station"][1]["name"], ", Temperature: ", hour_data_json["station"][1]["value"][0]["value"])
"""
# That worked! By changing the 0 after station to 1, I got new data, station name: Adelsö A , Temperature:  -0.6
# I can then make a for-loop and iterate through all the data.


# for i in range(len(hour_data_json["station"])):
#     print(f"""
#     station name: {hour_data_json["station"][i]["name"]},
#     Temperature: {hour_data_json["station"][i]["value"][0]["value"]},
#     Quality: {hour_data_json["station"][i]["value"][0]["quality"]}
#     """)

# I ran into an error. Let's check out i=5.
# Traceback (most recent call last):
#   File "C:\Code\Small-python-projects\api_request\newrequest.py", line 85, in <module>
#     Temperature: {hour_data_json["station"][i]["value"][0]["value"]},
# TypeError: 'NoneType' object is not subscriptable

# i=5
# print(f"""
#      station name: {hour_data_json["station"][i]["name"]},
#      Temperature: {hour_data_json["station"][i]}
#      """)

# As we can see here, some stations don't have any values.
# We can check if there's any entries in the key value to see if there's any value in the entry.
# I try again to get the previous data out, station name and values.
# # If no values I'll still print the station but input None as values.
# x=0


# for i in range(len(hour_data_json["station"])):
#     if hour_data_json["station"][i]["value"] is not None and hour_data_json["station"][i]["value"][0]["quality"] == "G":
#         print(f"""
#         Station name: {hour_data_json["station"][i]["name"]},
#         Temperature: {hour_data_json["station"][i]["value"][0]["value"]},
#         Quality: {hour_data_json["station"][i]["value"][0]["quality"]}
#         """)
#         x=x+1

# print(x)
# print(hour_data_json["station"][i])

"""
This works!
Let's assume we want to find more values than this though. Let's run the above print keys statement to see what information we might want from a station.
Result: dict_keys(['key', 'name', 'owner', 'ownerCategory', 'measuringStations', 'from', 'to', 'height', 'latitude', 'longitude', 'value']

Based on this list I may be interested in: key, name, owner, height, latitude, longitude and value.
Let's just make it easier and give them each a variable for our data-inquiry-functions.
"""
# station_id = hour_data_json["station"][i]["key"]
# station_name = hour_data_json["station"][i]["name"]
# station_owner = hour_data_json["station"][i]["owner"]
# station_longitude = hour_data_json["station"][i]["longitude"]
# station_latitude = hour_data_json["station"][i]["latitude"]
# station_temperature = hour_data_json["station"][i]["value"][0]["value"]
# station_value_quality = hour_data_json["station"][i]["value"][0]["quality"]
# station_value_date = hour_data_json["station"][i]["value"][0]["date"]

# # I also added variables for the less used variables below:
# station_height = hour_data_json["station"][i]["height"]
# station_to = hour_data_json["station"][i]["to"]
# station_from = hour_data_json["station"][i]["from"]
# measuring_Stations = hour_data_json["station"][i]["measuringStations"]
# station_owner_category = hour_data_json["station"][i]["ownerCategory"]
"""
I think this is plenty of information to be able to get started on the next iteration of the project, appending data to database.
Before that though, I want to create a function that can run continually to provide this data at a regular interval.
The goal of this function is to use the appropriate URL, get data from it and use the previously defined variables to post the data into a database.
href = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour/data.json"
"""

"""
Below follows my attempt at creating a script to be scheduled to run hourly.
"""
import psycopg2


def send_temperature_data_hourly():
    params = {
    'dbname': 'smhi_data',
    'user': 'postgres',
    'password': '',
    'port': 5432
    }
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()





    href = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour/data.json"
    data_text = requests.get(href).text
    hour_data_json = json.loads(data_text)
    cursor.execute("""
        select timestamp from temperature
        order by timestamp desc
        limit 1;
        """)
    # Check if there's a new timestamp in the first entry., if there's no new timestamp we assume there's no new data.
    latest_timestamp = cursor.fetchone()
    if latest_timestamp == hour_data_json["station"][0]["value"][0]["date"]:
        return None
    cursor.execute("""
    SELECT station_id from station;
    """)
    station_list = cursor.fetchall()
    for i in range(len(hour_data_json["station"])):
        if hour_data_json["station"][i]["value"] is not None:
            station_id = hour_data_json["station"][i]["key"]
            station_name = hour_data_json["station"][i]["name"]
            station_owner = hour_data_json["station"][i]["owner"]
            station_longitude = hour_data_json["station"][i]["longitude"]
            station_latitude = hour_data_json["station"][i]["latitude"]
            station_temperature = hour_data_json["station"][i]["value"][0]["value"]
            station_value_quality = hour_data_json["station"][i]["value"][0]["quality"]
            station_value_date = hour_data_json["station"][i]["value"][0]["date"]
            station_height = hour_data_json["station"][i]["height"]

            # I also added variables for the less used variables below:
            # station_to = hour_data_json["station"][i]["to"]
            # station_from = hour_data_json["station"][i]["from"]
            # measuring_Stations = hour_data_json["station"][i]["measuringStations"]
            # station_owner_category = hour_data_json["station"][i]["ownerCategory"]
            

        if station_id not in station_list:
            cursor.execute(f"""
            INSERT INTO station (station_id, name, owner, lon, lat, height ) VALUES
            ({station_id}, $${station_name}$$, $${station_owner}$$, {station_longitude}, {station_latitude}, {station_height});
        """)
            connection.commit()

        if hour_data_json["station"][i]["value"] is not None:
            cursor.execute(f"""
            INSERT INTO temperature (station_id, value, timestamp, quality) VALUES
            ({station_id}, {station_temperature}, {station_value_date}, '{station_value_quality}');
            """)
            connection.commit()
    cursor.close()
    connection.close()
    return None


            # Timestamp is in Unix Epoch Time
            # We may want to check before posting to database if timestamp is represented in database. Most likely we can just check the first value and do a query as:
            # select timestamp from temperature
            # order by timestamp DESC
            # limit 1
            # And compare to the timestamp of first entry.