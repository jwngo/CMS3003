
"""
API is provided by http://api.data.gov.sg/v1/environment/2-hour-weather-forecast
-----------------------------------------------------------------------------------------
function: getWeather(time)
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
            "area_metadata": [
                {
                  "name": "Ang Mo Kio",
                  "label_location": {
                    "latitude": 1.375,
                    "longitude": 103.839
                  }
                },
                {
                  "name": "Bedok",
                  "label_location": {
                    "latitude": 1.321,
                    "longitude": 103.924
                  }
                }
            ],
            "items": [
                {
                  "update_timestamp": "2019-03-07T11:08:53+08:00",
                  "timestamp": "2019-03-07T11:00:00+08:00",
                  "valid_period": {
                    "start": "2019-03-07T11:00:00+08:00",
                    "end": "2019-03-07T13:00:00+08:00"
                  },
                  "forecasts": [
                    {
                      "area": "Ang Mo Kio",
                      "forecast": "Partly Cloudy (Day)"
                    },
                    {
                      "area": "Bedok",
                      "forecast": "Partly Cloudy (Day)"
                    }
                ]
            }
        ],
        "api_info": {
            "status": "healthy"
        }
    }
-----------------------------------------------------------------------------------------
Requirments:
    requests installed
"""

import requests

def getWeather(time):
    if(len(time) < 11):
        parameters = {"date": time};
    else:
        parameters = {"data_time: time"};
    response = requests.get("http://api.data.gov.sg/v1/environment/2-hour-weather-forecast", params=parameters)
    data = response.json()
    if(response.status_code != 200):
        print(data["message"])
    else:
        return data

#test
#print(getWeather("2019-03-01"));
