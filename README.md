# F1 Telemetry & Pit Strategy Project

Real-time racing telemetry ingestion, prediction of optimal pit stop, and live dashboard.

## Quick Start
1. Install Docker and Docker Compose.
2. Clone this repository.
3. Run `docker-compose up --build`
4. Access:
   - Dash: http://localhost:8050
   - Grafana (optional): you can add Grafana service.
   - Neo4j Browser: http://localhost:7474

## Components
- MQTT broker (Mosquitto)
- Simulator (generates fake car data)
- Processor (subscribes, stores in SQL/MongoDB/Neo4j, predicts pit strategy)
- Dash (Plotly Dash dashboard)
- Databases: PostgreSQL, MongoDB, Neo4j

See `docs/` for architecture and report.
