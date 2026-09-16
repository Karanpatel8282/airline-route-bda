from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc

spark = SparkSession.builder \
    .appName("AirportAnalysis") \
    .getOrCreate()

# Read cleaned airport data
airports = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/airports_clean")

print("Total Airports:", airports.count())

# 1. Number of airports by country
print("\nAirports by Country")

country_airports = airports.groupBy("country") \
    .agg(count("*").alias("airport_count")) \
    .orderBy(desc("airport_count"))

country_airports.show(10)

# 2. Number of airports by type
print("\nAirports by Type")

airport_types = airports.groupBy("type") \
    .agg(count("*").alias("airport_count")) \
    .orderBy(desc("airport_count"))

airport_types.show()

# 3. Top cities by number of airports
print("\nTop Cities by Number of Airports")

city_airports = airports.groupBy("city", "country") \
    .agg(count("*").alias("airport_count")) \
    .orderBy(desc("airport_count"))

city_airports.show(10)

# Save analysis results
country_airports.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airport_analysis/country_airports")

airport_types.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airport_analysis/airport_types")

city_airports.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airport_analysis/city_airports")

print("\nAirport analysis completed successfully.")

spark.stop()