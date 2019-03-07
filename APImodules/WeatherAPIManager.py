
"""
API is provided by http://api.data.gov.sg/v1/environment/2-hour-weather-forecast
-----------------------------------------------------------------------------------------
function: getAllWeather(time)
parameter:
    time needs to be a string
    It can be in either one of the following formats:

    date and time:
    YYYY-MM-DD[T]HH:mm:ss
    Use this format to retrieve the latest forecast issued at that moment in time.

    date:
    YYYY-MM-DD
    Use this format to retrieve all of the forecasts issued for a certain day.
return:
    A python object that contains weather forecasts for multiple areas in Singapore
    Structure of the object:
        {
          "api_info": {
            "status": "healthy"
          },
          "area_metadata": [
            {
              "name": "string",
              "label_location": {
                "longitude": 0,
                "latitude": 0
              }
            }
          ],
          "items": [
            {
              "update_timestamp": "2019-03-07T07:56:25.548Z",
              "timestamp": "2019-03-07T07:56:25.548Z",
              "valid_period": {
                "start": "2019-03-07T07:56:25.548Z",
                "end": "2019-03-07T07:56:25.548Z"
              },
              "forecasts": [
                {
                  "area": "string",
                  "forecast": "string"
                }
              ]
            }
          ]
        }
    }
---------------------------------------------------------------------------------------
function: getWeatherByLocation(time, area)
parameter: both time and area are strings
return:
        {'AreaName': 'Forecast'}
-----------------------------------------------------------------------------------------
Requirments:
    requests installed
"""

import requests

def getAllWeather(time):
    if(len(time) < 11):
        parameters = {"date": time};
    else:
        parameters = {"data_time": time};
    response = requests.get("http://api.data.gov.sg/v1/environment/2-hour-weather-forecast", params=parameters)
    data = response.json()
    if(response.status_code != 200):
        print(data["message"])
    else:
        return data
    

def getWeatherByLocation(time, area):
    locationData = {};
    data = getAllWeather(time);
    for forcast in data["items"][0]["forecasts"] :
        if(forcast["area"] == area):
            locationData[area] = forcast["forecast"];
    if not locationData:
        print("Area not found.");
    return locationData;

#test
print(getWeatherByLocation("2019-03-01T00:00:00", "Bedok"));
