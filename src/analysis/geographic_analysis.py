from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, min, max, desc

spark = SparkSession.builder \
    .appName("GeographicAnalysis") \
    .getOrCreate()

# Read cleaned airport data
airports = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/airports_clean")

# Convert latitude and longitude to numeric values
airports = airports.withColumn(
    "latitude",
    col("latitude").cast("double")
).withColumn(
    "longitude",
    col("longitude").cast("double")
)

# Remove records without geographic coordinates
geo_airports = airports.filter(
    col("latitude").isNotNull() &
    col("longitude").isNotNull()
)

print("Airports with valid coordinates:", geo_airports.count())

# 1. Geographic distribution by country
print("\nGeographic Distribution by Country")

country_geo = geo_airports.groupBy("country") \
    .agg(
        count("*").alias("airport_count"),
        avg("latitude").alias("average_latitude"),
        avg("longitude").alias("average_longitude")
    ) \
    .orderBy(desc("airport_count"))

country_geo.show(10)

# 2. Latitude range
print("\nLatitude Range")

geo_airports.select(
    min("latitude").alias("minimum_latitude"),
    max("latitude").alias("maximum_latitude")
).show()

# 3. Longitude range
print("\nLongitude Range")

geo_airports.select(
    min("longitude").alias("minimum_longitude"),
    max("longitude").alias("maximum_longitude")
).show()

# Save geographic analysis
country_geo.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/geographic_analysis/country_geography")

print("\nGeographic analysis completed successfully.")

spark.stop()