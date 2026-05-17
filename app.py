from flask_cors import CORS
from flask import Flask, jsonify
from database import init_db
from routes.vehicles import vehicles
from routes.drivers import drivers
from routes.routes_api import routes_api
from routes.packages import packages

init_db()

app = Flask(__name__)
CORS(app, origins="*")

app.register_blueprint(vehicles, url_prefix="/vehicles")
app.register_blueprint(drivers, url_prefix="/drivers")
app.register_blueprint(routes_api, url_prefix="/routes")
app.register_blueprint(packages, url_prefix="/packages")


@app.route("/")
def home():
    return jsonify({"message": "Server Online"})


if __name__ == "__main__":
    app.run(debug=True)

