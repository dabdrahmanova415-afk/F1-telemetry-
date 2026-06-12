import json
import time

import mysql.connector
from pymongo import MongoClient
from neo4j import GraphDatabase
import paho.mqtt.client as mqtt


# ==========================
# MYSQL
# ==========================

def connect_mysql():
    while True:
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="telemetry"
            )

            print("[MYSQL] Connected")

            return conn

        except Exception as e:
            print(f"[MYSQL] Waiting... {e}")
            time.sleep(5)


mysql_conn = connect_mysql()

cursor = mysql_conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS laps(
    id INT AUTO_INCREMENT PRIMARY KEY,
    car VARCHAR(50),
    lap INT,
    speed INT,
    fuel FLOAT,
    tire_wear FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

mysql_conn.commit()


# ==========================
# MONGODB
# ==========================

def connect_mongo():
    while True:
        try:
            client = MongoClient(
                "mongodb://mongodb:27017/"
            )

            db = client["telemetry"]

            print("[MONGODB] Connected")

            return db["raw_data"]

        except Exception as e:
            print(f"[MONGODB] Waiting... {e}")
            time.sleep(5)


mongo_collection = connect_mongo()


# ==========================
# NEO4J
# ==========================

def connect_neo4j():
    while True:
        try:
            driver = GraphDatabase.driver(
                "bolt://neo4j:7687",
                auth=("neo4j", "testpass")
            )
            print("[NEO4J] Connected")
            return driver
        except Exception as e:
            print(f"[NEO4J] Waiting... {e}")
            time.sleep(5)
neo4j_driver = connect_neo4j()


# ==========================
# ANALYTICS
# ==========================

def pit_stop_needed(fuel, tire_wear):

    if fuel < 15:
        return True

    if tire_wear > 0.8:
        return True

    return False


# ==========================
# MQTT CALLBACK
# ==========================

def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode()

        data = json.loads(payload)

        car = data["car"]
        lap = data["lap"]
        speed = data["speed"]
        fuel = data["fuel"]
        tire_wear = data["tire_wear"]

        print(f"[MQTT] {data}")

        # ==========================
        # MYSQL
        # ==========================

        cursor.execute(
            """
            INSERT INTO laps(
                car,
                lap,
                speed,
                fuel,
                tire_wear
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                car,
                lap,
                speed,
                fuel,
                tire_wear
            )
        )

        mysql_conn.commit()

        print("[MYSQL] Data inserted")

        # ==========================
        # MONGODB
        # ==========================

        mongo_collection.insert_one(data)

        print("[MONGODB] Data inserted")

        # ==========================
        # NEO4J
        # ==========================

        with neo4j_driver.session() as session:
            session.run(
                """
                MERGE (c:Car {name:$car})
                MERGE (l:Lap {
                    number:$lap
                })
                MERGE (c)-[:COMPLETED]->(l)
                """,
                car=car,
                lap=lap
            )
            if tire_wear > 0.8:
                session.run(
                    """
                    MERGE (c:Car {name:$car})
                    CREATE (e:TireEvent {
                        wear:$wear
                    })
                    CREATE (c)-[:HIGH_WEAR]->(e)
                    """,
                    car=car,
                    wear=tire_wear
                )

        print("[NEO4J] Data inserted")
        # ==========================
        # ANALYTICS
        # ==========================

        if pit_stop_needed(
            fuel,
            tire_wear
        ):

            print(
                f"[PIT STOP RECOMMENDED] "
                f"car={car} "
                f"fuel={fuel} "
                f"wear={tire_wear}"
            )

    except Exception as e:

        print(
            f"[ERROR] "
            f"{e}"
        )


# ==========================
# MQTT CLIENT
# ==========================

client = mqtt.Client()
client.on_message = on_message
while True:
    try:
        client.connect(
            "mosquitto",
            1883,
            60
        )
        break
    except Exception as e:

        print(
            f"[MQTT] Waiting broker... {e}"
        )
        time.sleep(5)
client.subscribe("f1/telemetry")
print(
    "[MQTT] Subscribed to f1/telemetry"
)
client.loop_forever()

