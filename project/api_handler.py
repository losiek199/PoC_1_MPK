import json
import os.path
from flask import Flask, render_template, abort, request, jsonify, Response, send_file
from flask_restful import Api
import project.db_controller as db

app = Flask(__name__)
api = Api(app)

print(db.Base.mro())
def run_server():
    app.run(debug=True)

@app.route("/", methods=['GET'])
def welcome():
    return render_template('welcome.html')

@app.route("/routes", methods=['GET'])
def routes():
    cities = db.select_cities()
    return render_template('routes_main.html', cities=cities)

@app.route("/routes/<city_name>", methods=['GET'])
def route(city_name):
    try:
        routes = db.select_routes_for_city(city_name)
        return render_template('routes.html', city_name=city_name, routes=jsonify(routes).data)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')


@app.route('/trips', methods=['GET'])
def trips_city():
    cities = db.select_cities()
    return render_template('trips_city.html', cities=cities)

@app.route('/trips/<city_name>', methods=['GET'])
def trips_city_file(city_name):
    try:
        trips = db.select_city_trips(city_name)
        with open('trips.json', 'w') as file:
            file.write(str(jsonify(trips)))
        return send_file(os.path.abspath(file), as_attachment=True)
    except Exception:
        abort(404)

"""API methods"""
@app.route("/api/cities", methods=['GET', 'POST'], )
def api_cities():
    if request.method == 'POST':
        db_resp = db.insert_city_row(request.json)
        if db_resp == 0:
            return Response(status=409, response=(f'{json.loads(request.data)} already exists'))
        else:
            return Response(status=200, response=request.data, mimetype='application/json')
    else:
        data = db.select_cities()
        rdict = {'cities': [dict(val) for val in data]}
        return jsonify(rdict)


@app.route("/api/routes/<city_name>", methods=['GET'])
def api_city_routes(city_name):
    try:
        routes = db.select_routes_for_city(city_name)
        return jsonify(routes)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')

@app.route("/api/trips/<city_name>", methods=['GET'])
def trips_city_denormalized(city_name):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 200, type=int)
    try:
        trips = db.select_city_trips(city_name)
        trips_paginated = trips.query.paginate(page, per_page)
        print(trips_paginated)
        return jsonify(trips_paginated)
    except Exception as e:
        return Response(str(e), status=400, mimetype='apllication/json')

