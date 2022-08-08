
from crypt import methods
from distutils.log import debug
import json,os,requests
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


def getResponse(res):
    """
    "queryResult": {
        "queryText": "weather in LA today",
        "parameters": {
                "date-time": "2022-08-08T12:00:00+05:30",
                "geo-city": "Los Angeles"
    },...}

    """
    

    query = res.get('queryResult')
    parameters = query.get('parameters')
    city = parameters.get("geo-city")
    date = parameters.get('date-time')

    web_api = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7fa4fc93e21f5c2987bd51291b001272").json()
    weather_list = web_api['list']

    description_condition = ""

    for i in weather_list:
        print(i['dt_txt'] ,date)
        if i['dt_txt'] in date:
            description_condition = i['weather'][0]['description']
            main_condition = i['weather'][0]['main']
        else:
            date_error = "Date is  not available"

    if description_condition:
        dialog_response = f"The forecast for {city} on {date} is {description_condition}({main_condition})"
    else:
        dialog_response = date_error

    context = {
        "speech":dialog_response,
        "displayText":dialog_response,
        "source":"apiai-weather-webhook"
    }

    return context



app.route("/webhook",methods=["POST"])
def webbhook():
    req = request.get_json(silent = True , force = True)
    print(json.dumps(req,indent=4))

    res = getResponse(req)
    res = json.dumps(res,indent=4)
    flask_response = make_response(res)
    flask_response.headers['Content-Type'] = "application/json"
    return flask_response

if __name__ =="__main__":
    port  = int(os.getenv("PORT",5000))
    print("starting app on port",port)
    app.run(debug=False,port=port,host="0.0.0.0")