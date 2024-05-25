# import requests
#
# url = "https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp"
#
# querystring = {"number":"+998993590562","country":"UZ"}
#
# headers = {
# 	"X-RapidAPI-Key": "33c3a6de00msh01e1b64b8b70110p17d66ajsn623a0562b923",
# 	"X-RapidAPI-Host": "phonenumbervalidatefree.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers, params=querystring)
#
# print(response.json())

#
from fastapi import FastAPI
from pydantic import BaseModel
import math

# app = FastAPI()
#
#
#

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the Earth.

    Parameters:
    lat1, lon1 : float : Latitude and longitude of the first point
    lat2, lon2 : float : Latitude and longitude of the second point

    Returns:
    float : Distance between the two points in kilometers
    """
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance



print("Km: ",round(haversine_distance(41.30397199444702, 69.24635858999734,41.23765534838305, 69.21580286724335),1 ))



