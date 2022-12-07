from flask import Flask, render_template, abort, request, jsonify, Response, redirect
from flask_restful import Api, Resource
from markupsafe import escape
import db_controller

app = Flask(__name__)
api = Api(app)

def run_server():
    app.run(debug=True)

@app.route("/", methods=['GET'])
def welcome():
    return render_template('welcome.html')

@app.route("/routes")
def routes():
     return render_template('routes_main.html')

@app.route("/routes/<city_name>", methods=['GET'])
def route(city_name):
    try:
        conn = db_controller.initialize_connection()
        routes = db_controller.select_routes_for_city(conn, city_name)
        return render_template('routes.html', city_name=city_name, routes=jsonify(routes).data)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')

@app.route('/trips/<city_name>')
def trips_city(city_name):
    return render_template('trips_city.html')


"""API methods"""
@app.route("/api/cities", methods=['GET', 'POST'])
def api_cities():
    conn = db_controller.initialize_connection()
    if request.method == 'POST':
        try:
            db_controller.insert_data_row(conn, 'cities', tuple(request.form['city_name']))
            return Response("Success", status=200)
        except Exception as e:
            return Response(str(e), status=400, mimetype='application/json')
    else:
        data = db_controller.select_from_table(conn, 'cities')
        return jsonify(data)

@app.route("/api/routes/<city_name>")
def api_city_routes(city_name):
    try:
        conn = db_controller.initialize_connection()
        routes = db_controller.select_routes_for_city(conn, city_name)
        return jsonify(routes)
    except Exception as e:
        return Response(str(e), status=404, mimetype='application/json')

@app.route("/api/trips/<city_name>")
def trips_city_denormalized(city_name):
    try:
        conn = db_controller.initialize_connection()
    except Exception as e:
        return Response(str(e), status=404, mimetype='apllication/json')


