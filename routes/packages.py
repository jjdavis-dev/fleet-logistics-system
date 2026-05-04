from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

packages = Blueprint("packages", __name__)

@packages.route("/")
def get_packages():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from packages order by package_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@packages.route("/", methods=["POST"])
def create_package():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        insert into packages (description, weight, route_id)
        values (%s, %s, %s)
    """, (data["description"], data["weight"], data["route_id"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Package Created"}), 201

@packages.route("/<int:id>", methods=["PUT"])
def update_package(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        update packages
        set description = %s, weight = %s, route_id = %s
        where package_id = %s
    """, (data["description"], data["weight"], data["route_id"], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Package Updated"})

@packages.route("/<int:id>", methods=["DELETE"])
def delete_package(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("delete from packages where package_id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Package Deleted"})