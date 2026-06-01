# System Architecture

Data flow:
Simulator -> MQTT -> Processor -> (PostgreSQL, MongoDB, Neo4j) -> Dash

- **Simulator**: publishes telemetry, tires, fuel, events to MQTT topics.
- **Processor**: subscribes, parses JSON, writes raw data to MongoDB, aggregates laps to PostgreSQL, updates graph in Neo4j, and runs ML predictor every 3 laps.
- **Predictor**: uses RandomForestRegressor (trained on synthetic data) to predict laps left before optimal pit stop.
- **Dash**: real-time charts of speed, RPM, tire wear; shows pit recommendation.

## Technologies
- MQTT: Eclipse Mosquitto
- Python: paho-mqtt, psycopg2, pymongo, neo4j, scikit-learn, pandas, dash
- DB: MySQL (structured laps), MongoDB (raw telemetry), Neo4j (graph of cars, tracks, tyres, strategies)
- Containerization: Docker Compose
