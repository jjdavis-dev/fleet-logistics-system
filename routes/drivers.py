from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

drivers = Blueprint("drivers", __name__)

@drivers.route("/")
def get_drivers():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from drivers order by driver_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@drivers.route("/", methods=["POST"])
def create_driver():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        insert into drivers (name, license_type)
        values (%s, %s)
    """, (data["name"], data["license_type"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Driver Created"}), 201

@drivers.route("/<int:id>", methods=["PUT"])
def update_driver(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        update drivers
        set name = %s, license_type = %s
        where driver_id = %s
    """, (data["name"], data["license_type"], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Driver Updated"})

@drivers.route("/<int:id>", methods=["DELETE"])
def delete_driver(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("delete from drivers where driver_id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Driver Deleted"})