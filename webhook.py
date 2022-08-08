import json
from multiprocessing import context
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

def processRequest(req):
 
    # if req.["result"].["action"] != "fetchWeatherForecast":
    #     return {}
    result = req["queryResult"]
    parameters = result["parameters"]
    city = parameters["geo-city"]
    date = parameters["date"]
    if city is None:
        return None
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=7fa4fc93e21f5c2987bd51291b001272')
    json_object = r.json()
    weather=json_object['list']
    condition = "something broke"
    main = "Error"
    for i in range(0,30):
        print(date.split("T")[0], weather[i]['dt_txt'])
        if date.split("T")[0] in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']
            main = weather[i]['weather'][0]['main']
            break
    
    speech = "The forecast for "+city+ "for "+date+" is "+condition+f"({main})"
    context =                {
                "fulfillmentMessages": [
                    {
                    "text": {
                        "text": [
                        f"{speech}"
                        ]
                    }
                    }
                ]
                }
    return context
    

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    
    res = json.dumps(res, indent=4)
    # print(res]
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















