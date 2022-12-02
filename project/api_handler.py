from flask import Flask, render_template
from flask_restful import Api, Resource
from markupsafe import escape


app = Flask(__name__)
api = Api(app)


def run_server():
    app.run(debug=True)

@app.route("/")
def hello_world():
    return render_template('welcome.html')

@app.route("/welcome/<name>")
def hello_user(name):
    return f"<p>Hello, {escape(name)}!</p>"
