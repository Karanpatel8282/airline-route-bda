import pandas as pd
from pathlib import Path
from connection import driver

BASE_PATH = Path("data/processed")


def read_spark_csv(folder):
    files = list(folder.glob("part-*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV file found in {folder}")

    return pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )


airlines = read_spark_csv(BASE_PATH / "airlines_clean")
airports = read_spark_csv(BASE_PATH / "airports_clean")
routes = read_spark_csv(BASE_PATH / "routes_clean")

print("Airlines:", len(airlines))
print("Airports:", len(airports))
print("Routes:", len(routes))


def create_graph():
    with driver.session() as session:

        session.run("""
            CREATE CONSTRAINT airline_id_unique IF NOT EXISTS
            FOR (a:Airline)
            REQUIRE a.airline_id IS UNIQUE
        """)

        session.run("""
            CREATE CONSTRAINT airport_id_unique IF NOT EXISTS
            FOR (a:Airport)
            REQUIRE a.airport_id IS UNIQUE
        """)

        print("Constraints created.")

        for _, row in airlines.iterrows():
            session.run("""
                MERGE (a:Airline {airline_id: $airline_id})
                SET a.name = $name,
                    a.country = $country,
                    a.iata = $iata,
                    a.icao = $icao,
                    a.active = $active
            """,
            airline_id=int(row["airline_id"]),
            name=str(row["name"]),
            country=str(row["country"]),
            iata=str(row["iata"]),
            icao=str(row["icao"]),
            active=str(row["active"])
            )

        print("Airline nodes created.")

        for _, row in airports.iterrows():
            session.run("""
                MERGE (a:Airport {airport_id: $airport_id})
                SET a.name = $name,
                    a.city = $city,
                    a.country = $country,
                    a.iata = $iata,
                    a.icao = $icao,
                    a.latitude = $latitude,
                    a.longitude = $longitude
            """,
            airport_id=int(row["airport_id"]),
            name=str(row["name"]),
            city=str(row["city"]),
            country=str(row["country"]),
            iata=str(row["iata"]),
            icao=str(row["icao"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"])
            )

        print("Airport nodes created.")

        for _, row in routes.iterrows():
            session.run("""
                MATCH (airline:Airline {airline_id: $airline_id})
                MATCH (source:Airport {airport_id: $source_id})
                MATCH (destination:Airport {airport_id: $destination_id})

                MERGE (source)-[r:ROUTE {
                    airline_id: $airline_id
                }]->(destination)

                SET r.airline_code = $airline_code,
                    r.codeshare = $codeshare,
                    r.stops = $stops,
                    r.equipment = $equipment

                MERGE (airline)-[:OPERATES]->(source)
            """,
            airline_id=int(row["airline_id"]),
            source_id=int(row["source_airport_id"]),
            destination_id=int(row["destination_airport_id"]),
            airline_code=str(row["airline"]),
            codeshare=str(row["codeshare"]),
            stops=int(row["stops"]),
            equipment=str(row["equipment"])
            )

        print("Route relationships created.")

if __name__ == "__main__":
    create_graph()
    driver.close()
print("Airline, Airport, and Route data imported successfully.")