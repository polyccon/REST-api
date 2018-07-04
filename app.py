#!/usr/bin/env python3
import requests, json
from flask import Flask, jsonify, request, abort, make_response, render_template
from flask import g
from datetime import datetime
import googlemaps


app = Flask(__name__)

def _parse_request_body():
    """Extract data type from request body."""
    request_body = request.get_json()
    try:
        id_ = request_body['id']
        items = request_body['items']

    except KeyError:
        # Missing necessary fields.
        response_body = {
            'error':
            "'id', 'items' key in request body"
        }
        abort(make_response(jsonify(response_body), 400))
    return id_, items

@app.route('/healthz', methods=['GET'])
def healthz():
    return ('', 200)

@app.route("/")
def hello():
    return render_template('home.html', name = 'user')

@app.route('/viewcrime', methods=['GET', 'POST'])
def viewcrime():
    keyword = request.form['keyword']
    location = request.form['location']
    print (keyword, 'location', location)
    try:
        gmaps = googlemaps.Client(key=g.GKEY)

        # Geocoding an address
        geocode_result = gmaps.geocode(location)
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        ll = str(latitude) + ', ' + str(longitude)
        url = 'https://data.police.uk/api/crimes-street/all-crime?'


        params = dict(
            lat = latitude,
            lng = longitude
        )
        resp = requests.get(url=url, params=params)

        data = json.loads(resp.text)
        results_dict = {}
        for item in data:
            if not results_dict.get(item['category']):
                results_dict[item['category']] = 1
            else:
                results_dict[item['category']] += 1

        return render_template('results.html', results = results_dict)


    except Exception as e:
        print ('Error:', e)
        return 'Unable to track location, please enter a different address'




if __name__ == '__main__':
    app.run(debug= True)
