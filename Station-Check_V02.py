import json
import xmltodict
import http.client
import random as r
from datetime import date
import datetime

# Konstanten für API-Parameter
DB_CLIENT_ID = "9e6dcafbff6eee1b2248e777ae5f9828"
DB_API_KEY = "abd6cd3f5a309e3c84f3928d03ff7ee0"
today = date.today()
now = datetime.datetime.now()
hour = "0" + str(now.hour)
date = today.strftime("%y%m%d")

def get_station_timetable(station_eva, date, hour):
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    headers = {
        'DB-Client-Id': DB_CLIENT_ID,
        'DB-Api-Key': DB_API_KEY,
        'accept': "application/xml, application/json"
    }
    print(station_eva, date, hour)
    conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/plan/{station_eva}/{date}/{hour}", headers=headers)
    response = conn.getresponse()
    xml_data = response.read().decode("utf-8")
    conn.close()
    return xml_data

def get_station_data(station_search):
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    headers = {
        'DB-Client-Id': DB_CLIENT_ID,
        'DB-Api-Key': DB_API_KEY,
        'accept': "application/xml, application/json"
    }
    conn.request("GET", f"/db-api-marketplace/apis/station-data/v2/stations?searchstring={station_search}*", headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    conn.close()
    return data

def get_station_name(data):
    return data["result"][0]["evaNumbers"][0]["number"]

def set_station_value(timetable_data, num):
    s = timetable_data["timetable"]["s"]
    ar_ppth = s[1]["ar"]["@ppth"]
    dp_ppth = s[num]["dp"]["@ppth"]
    from_list = ar_ppth[0:30].split("|")
    print(ar_ppth)
    to_list = dp_ppth.split("|")
    from_station = from_list[0]
    to_station = to_list[-1]
    arr_time = s[num]["ar"]["@pt"]
    line = s[num]["tl"]["@c"] + s[num]["ar"]["@l"]
    arrival = f"{arr_time[6:8]}:{arr_time[8:10]}"
    return to_station, from_station, line, arrival

def convert_xml_to_dict(xml_data):
    parsed_data = xmltodict.parse(xml_data)
    return parsed_data

def randomize_data(data):
    data = r.randint(0,len(data["timetable"]["s"]))
    return data

def output_data(to_station, from_station, line, arrival):
    print("********************************************DEBUG********************************************")
    print(f"Einfahrt {line} aus {from_station} nach {to_station} um {arrival}")

def start(station, hour, date):
    station_data = get_station_data(station)
    station_eva = get_station_name(station_data)
    timetable_data = get_station_timetable(station_eva, hour, date)
    json_data = convert_xml_to_dict(timetable_data)
    num = randomize_data(json_data)
    to, from_station, line, arrival = set_station_value(json_data, num)
    output_data(to, from_station, line, arrival)

if __name__ == "__main__":
    start("Berliner", date, hour)