import os
from pathlib import Path

from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / "config" / ".env")

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

missing_variables = [
    name
    for name, value in {
        "NEO4J_URI": URI,
        "NEO4J_USERNAME": USERNAME,
        "NEO4J_PASSWORD": PASSWORD,
    }.items()
    if not value
]
if missing_variables:
    raise RuntimeError(
        "Missing required Neo4j environment variables: "
        + ", ".join(missing_variables)
    )

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def close_driver():
    driver.close()