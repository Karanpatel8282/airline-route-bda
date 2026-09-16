from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc

spark = SparkSession.builder \
    .appName("AirportFeatureEngineering") \
    .getOrCreate()

# Read cleaned routes data
routes = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/routes_clean")

# Calculate outgoing connectivity
outgoing = routes.groupBy("source_airport") \
    .agg(count("*").alias("outgoing_routes"))

# Calculate incoming connectivity
incoming = routes.groupBy("destination_airport") \
    .agg(count("*").alias("incoming_routes"))

# Combine incoming and outgoing connectivity
airport_features = outgoing.join(
    incoming,
    outgoing.source_airport == incoming.destination_airport,
    "outer"
).select(
    col("source_airport").alias("airport"),
    col("outgoing_routes"),
    col("incoming_routes")
)

# Replace missing values with 0
airport_features = airport_features.fillna(0)

# Calculate total connectivity
airport_features = airport_features.withColumn(
    "total_connectivity",
    col("outgoing_routes") + col("incoming_routes")
)

# Rank airports by connectivity
airport_features = airport_features.orderBy(
    desc("total_connectivity")
)

print("Top Connected Airports")
airport_features.show(20)

print("Airport Feature Schema")
airport_features.printSchema()

# Save features
airport_features.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airport_analysis/airport_features")

print("Airport feature engineering completed successfully.")

spark.stop()