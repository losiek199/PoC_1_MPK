import json
import math
from flask import Flask, render_template, abort, request, jsonify, Response
from flask_restful import Api
import project.db_controller as db

app = Flask(__name__)
api = Api(app)

def run_server():
    app.run(debug=True, use_reloader=False)

@app.route("/", methods=['GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/cities', methods=['GET'])
def cities():
    session = db.Session()
    cities = db.select_cities(session)
    return render_template('cities.html', cities=cities)

@app.route("/routes", methods=['GET'])
def routes():
    session = db.Session()
    cities = db.select_cities(session)
    return render_template('routes_main.html', cities=cities)

@app.route("/routes/<city_name>", methods=['GET'])
def route(city_name):
    session = db.Session()
    try:
        routes = db.select_routes_for_city(session, city_name)
        return render_template('routes.html', city_name=city_name, routes=routes)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')


@app.route('/trips', methods=['GET'])
def trips_city():
    session = db.Session()
    cities = db.select_cities(session)
    return render_template('trips_city.html', cities=cities)

@app.route('/trips/<city_name>', methods=['GET'])
@app.route('/trips/<city_name>/<int:page>', methods=['GET'])
def trips_city_list(city_name, page=0):
    session = db.Session()
    per_page = 100
    try:
        pg_cnt = math.ceil(db.select_count_from_city_trips(session, city_name)/per_page)
        trips = db.select_city_trips(session, page, per_page, city_name)
        return render_template('trips_list.html',
                               city_name=city_name,
                               trips=trips,
                               page=page,
                               page_cnt=pg_cnt)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')

"""API methods"""
@app.route("/api/cities", methods=['GET', 'POST'], )
def api_cities():
    session = db.Session()
    if request.method == 'POST':
        db_resp = db.insert_city_row(session, request.json)
        if db_resp == 0:
            return Response(status=409, response=(f'{json.loads(request.data)} already exists'))
        else:
            return Response(status=200, response=request.data, mimetype='application/json')
    else:
        data = db.select_cities(session)
        rdict = {'cities': [dict(val) for val in data]}
        return jsonify(rdict)


@app.route("/api/routes/<city_name>", methods=['GET'])
def api_city_routes(city_name):
    session = db.Session()
    try:
        routes = db.select_routes_for_city(session, city_name)
        return {'count': len(routes), 'routes': [dict(val) for val in routes]}
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')


@app.route("/api/trips/<city_name>")
@app.route("/api/trips/<city_name>/<int:page>", methods=['GET'])
def trips_city_denormalized(city_name, page=0):
    """api endpoint returns paginated """
    session = db.Session()
    page_size = 100
    pg_cnt = math.ceil(db.select_count_from_city_trips(session, city_name)/page_size)
    try:
        result = db.select_city_trips(session, page, page_size, city_name)
        return {'page': page, 'per_page':page_size, 'page_count': pg_cnt, 'trips': result}
    except Exception as e:
        return Response(str(e), status=400, mimetype='apllication/json')

