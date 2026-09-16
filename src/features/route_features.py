from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, desc

spark = SparkSession.builder \
    .appName("RouteFeatureEngineering") \
    .getOrCreate()

# Read cleaned routes data
routes = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/routes_clean")

# Convert stops to numeric
routes = routes.withColumn(
    "stops",
    col("stops").cast("integer")
)

# Create codeshare indicator
routes = routes.withColumn(
    "is_codeshare",
    when(col("codeshare") == "Y", 1).otherwise(0)
)

# 1. Direct vs multi-stop routes
route_features = routes.groupBy("source_airport", "destination_airport") \
    .agg(
        count("*").alias("airline_count"),
        count(when(col("stops") == 0, True)).alias("direct_routes"),
        count(when(col("stops") > 0, True)).alias("multi_stop_routes"),
        count(when(col("is_codeshare") == 1, True)).alias("codeshare_routes")
    )

print("Top Route Features")
route_features.orderBy(
    desc("airline_count")
).show(20)

print("Route Feature Schema")
route_features.printSchema()

# Save route features
route_features.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/route_analysis/route_features")

print("Route feature engineering completed successfully.")

spark.stop()