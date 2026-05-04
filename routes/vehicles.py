from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

vehicles = Blueprint("vehicles", __name__)

@vehicles.route("/")
def get_vehicles():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from vehicles order by vehicle_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@vehicles.route("/", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        insert into vehicles (license_plate, model)
        values (%s, %s)
    """, (data["license_plate"], data["model"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Vehicle Created"}), 201

@vehicles.route("/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        update vehicles
        set license_plate = %s, model = %s
        where vehicle_id = %s
    """, (data["license_plate"], data["model"], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Vehicle Updated"})

@vehicles.route("/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("delete from vehicles where vehicle_id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Vehicle Deleted"})