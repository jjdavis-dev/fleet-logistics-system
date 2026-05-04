from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

routes_api = Blueprint("routes_api", __name__)


@routes_api.route("/")
def get_routes():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
                    select * from routes
                    order by route_id
            """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)


@routes_api.route("/", methods=["POST"])
def create_route():
    try:
        conn = get_connection()
        cur = conn.cursor()
        data = request.get_json()

        cur.execute("""
                    insert into routes
                    (route_date, service_zone, driver_id)
                    values
                    (%s, %s, %s)
            """, (data["route_date"], data["service_zone"], data["driver_id"]))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201


@routes_api.route("/<int:id>", methods=["PUT"])
def update_route(id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        data = request.get_json()

        cur.execute("""
                    update routes
                    set route_date = %s,
                        service_zone = %s,
                        driver_id = %s
                    where route_id = %s
            """, (data["route_date"], data["service_zone"], data["driver_id"], id))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201


@routes_api.route("/<int:id>", methods=["DELETE"])
def delete_route(id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
                    delete from routes
                    where route_id = %s
            """, (id,))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201