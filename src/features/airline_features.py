from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc

spark = SparkSession.builder \
    .appName("AirlineFeatureEngineering") \
    .getOrCreate()

# Read cleaned routes data
routes = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/routes_clean")

# Calculate total routes operated by each airline
airline_features = routes.groupBy("airline", "airline_id") \
    .agg(
        count("*").alias("total_routes")
    ) \
    .orderBy(desc("total_routes"))

print("Top Airlines by Route Coverage")
airline_features.show(20)

print("Airline Feature Schema")
airline_features.printSchema()

# Save features
airline_features.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airline_analysis/airline_features")

print("Airline feature engineering completed successfully.")

spark.stop()