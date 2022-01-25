from genericpath import exists
from flask import Flask
import flask
import requests
import json
import os

app = Flask(__name__)

cloudsConverted = []
response = requests.get('https://api.aiven.io/v1/clouds')

with open('./tmp/clouds.tmp.json', 'w') as f:
    f.write(response.text)

with open('./tmp/clouds.tmp.json', 'r') as f:
    data = json.loads(f.read())

with open('./tmp/clouds.json', 'w') as f:
    clouds = data['clouds']
    for result in clouds:
        provider = result['cloud_name'].split('-')[0]
        x = {"description": result['cloud_description'], "name": result['cloud_name'], "latitude": result['geo_latitude'], "longitude": result['geo_longitude'], "region": result['geo_region'], "provider": provider}
        cloudsConverted.append(x)

    json.dump(cloudsConverted, f)
        

@app.route("/clouds")
def clouds():
    with open('./tmp/clouds.json', 'r') as f:
        data = json.loads(f.read())
        response = flask.json.jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == "__main__":
    app.run()