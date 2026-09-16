from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc

spark = SparkSession.builder \
    .appName("RouteAnalysis") \
    .getOrCreate()

# Read cleaned routes data
routes = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/routes_clean")

print("Total Routes:", routes.count())

# 1. Top airlines by number of routes
print("\nTop Airlines by Number of Routes")

top_airlines = routes.groupBy("airline") \
    .agg(count("*").alias("route_count")) \
    .orderBy(desc("route_count"))

top_airlines.show(10)

# 2. Top source airports
print("\nTop Source Airports")

top_source_airports = routes.groupBy("source_airport") \
    .agg(count("*").alias("outgoing_routes")) \
    .orderBy(desc("outgoing_routes"))

top_source_airports.show(10)

# 3. Top destination airports
print("\nTop Destination Airports")

top_destination_airports = routes.groupBy("destination_airport") \
    .agg(count("*").alias("incoming_routes")) \
    .orderBy(desc("incoming_routes"))

top_destination_airports.show(10)

# 4. Most connected airport pairs
print("\nMost Frequent Airport Connections")

airport_connections = routes.groupBy(
    "source_airport",
    "destination_airport"
).agg(
    count("*").alias("route_count")
).orderBy(desc("route_count"))

airport_connections.show(10)

# Save route analysis results
top_airlines.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/route_analysis/top_airlines")

top_source_airports.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/route_analysis/top_source_airports")

top_destination_airports.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/route_analysis/top_destination_airports")

airport_connections.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/route_analysis/airport_connections")

print("\nRoute analysis completed successfully.")

spark.stop()