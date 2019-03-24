
// API is provided by https://data.gov.sg/dataset/weather-forecast
// -----------------------------------------------------------------------------------------
// function: getAllWeather(time)
// parameter:
//     time needs to be a string
//     It can be in either one of the following formats:

//     date and time:
//     YYYY-MM-DD[T]HH:mm:ss
//     Use this format to retrieve the latest forecast issued at that moment in time.

//     date:
//     YYYY-MM-DD
//     Use this format to retrieve all of the forecasts issued for a certain day.
// return:
//     A python object that contains weather forecasts for multiple areas in Singapore
//     Structure of the object:
//         {
//           "api_info": {
//             "status": "healthy"
//           },
//           "area_metadata": [
//             {
//               "name": "string",
//               "label_location": {
//                 "longitude": 0,
//                 "latitude": 0
//               }
//             }
//           ],
//           "items": [
//             {
//               "update_timestamp": "2019-03-07T07:56:25.548Z",
//               "timestamp": "2019-03-07T07:56:25.548Z",
//               "valid_period": {
//                 "start": "2019-03-07T07:56:25.548Z",
//                 "end": "2019-03-07T07:56:25.548Z"
//               },
//               "forecasts": [
//                 {
//                   "area": "string",
//                   "forecast": "string"
//                 }
//               ]
//             }
//           ]
//         }
//     }

function getAllWeather(time, callback){
    parameter = "";
    if(time.length > 11){
      parameter = "date_time"
    }
    else{
      parameter = "date"
    }
    var url = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        //console.log(JSON.parse(this.responseText))
        var allData = JSON.parse(this.responseText)
        allData = reorganizeData(allData)
        if (typeof callback === "function") {
          // apply() sets the meaning of "this" in the callback
          callback(allData);
        }
      }
    };
    xhttp.open("GET", url+"?"+parameter+"="+time, true)
    xhttp.send()
  }
  
  function reorganizeData(allData){
    var result = []
    var arr = allData.area_metadata
    for(var i = 0, len = arr.length; i < len; i++){
      result.push(arr[i])
    }
    for(i = 0, len1 = result.length; i < len1; i++){
      forecasts = allData.items[0].forecasts
      for(var j = 0, len2 = forecasts.length; j < len2; j++){
          if(forecasts[j].area == result[i].name){
              result[i].forecast = forecasts[j].forecast
          }
      }
      result[i].timeStamp = allData.items[0].timestamp
    }
    return result
  }
  
  getAllWeather("2019-03-03", console.log)
  
  