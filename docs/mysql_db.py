import mysql.connector
def get_mysql_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="telemetry"
    )

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laps(
        id INT AUTO_INCREMENT PRIMARY KEY,
        car VARCHAR(50),
        lap INT,
        speed INT
    )
    """)

    conn.commit()