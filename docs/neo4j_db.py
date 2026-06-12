from neo4j import GraphDatabase

def get_driver():

    driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "testpass")
)

driver.verify_connectivity()