import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        sslmode=os.getenv("DB_SSLMODE")
    )

    cur = conn.cursor()
    cur.execute("set search_path to logistics;")
    cur.close()

    
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

                create schema if not exists logistics;

                set search_path to logistics;
                
                create table if not exists vehicles
                (
                    vehicle_id serial primary key,
                    license_plate varchar(50) unique,
                    model varchar(100)
                );

                create table if not exists drivers
                (
                    driver_id serial primary key,
                    name varchar(100),
                    license_type varchar(50),
                    vehicle_id int unique references vehicles(vehicle_id)
                );

                create table if not exists routes
                (
                    route_id serial primary key,
                    route_date date,
                    service_zone varchar(100),
                    driver_id int references drivers(driver_id)
                );

                create table if not exists packages
                (
                    package_id serial primary key,
                    description text,
                    weight decimal(10, 2),
                    route_id int references routes(route_id)
                );

        """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database Ready!")