from flask import Flask, render_template, abort, request, jsonify
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

@app.route("/routes", methods=['GET'])
def routes_main():
    conn = db_controller.initialize_connection()
    data = db_controller.select_from_table(conn, 'cities')
    return render_template('routes_main.html', cities=data)

@app.route("/routes/<city_name>", methods=['GET'])
def route(city_name):
    try:
        conn = db_controller.initialize_connection()
        routes = db_controller.get_routes_for_city(conn, city_name)
        return render_template('routes.html', city_name=city_name, routes=jsonify(routes).data)
    except Exception as e:
        return render_template('error.html',  error=str(e))

@app.route("/cities", methods=['GET'])
def cities():
    conn = db_controller.initialize_connection()
    data = db_controller.select_from_table(conn, 'cities')
    return render_template('cities_data.html', cities=data)

@app.route("/api/cities")
def api_cities():
    conn = db_controller.initialize_connection()
    data = db_controller.select_from_table(conn, 'cities')
    return render_template('cities_data.html', cities=data)

@app.route("/api/routes/<city_name>")
def api_city_routes(city_name):
    try:
        conn = db_controller.initialize_connection()
        routes = db_controller.get_routes_for_city(conn, city_name)
        return jsonify(routes)
    except Exception as e:
        print('test')
        return render_template('error.html',  error=str(e))
