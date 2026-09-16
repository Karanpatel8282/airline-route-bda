from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc

spark = SparkSession.builder \
    .appName("AirlineAnalysis") \
    .getOrCreate()

# Read cleaned airline data
airlines = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/processed/airlines_clean")

print("Total Airlines:", airlines.count())

# 1. Airlines by country
print("\nAirlines by Country")

airlines_by_country = airlines.groupBy("country") \
    .agg(count("*").alias("airline_count")) \
    .orderBy(desc("airline_count"))

airlines_by_country.show(10)

# 2. Active vs inactive airlines
print("\nAirlines by Active Status")

airlines_by_status = airlines.groupBy("active") \
    .agg(count("*").alias("airline_count")) \
    .orderBy(desc("airline_count"))

airlines_by_status.show()

# 3. Airlines with IATA codes
print("\nAirlines with IATA Codes")

iata_airlines = airlines.filter(
    col("iata").isNotNull() & (col("iata") != "")
)

print("Airlines with IATA:", iata_airlines.count())

# Save analysis results
airlines_by_country.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airline_analysis/airlines_by_country")

airlines_by_status.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/output/airline_analysis/airlines_by_status")

print("\nAirline analysis completed successfully.")

spark.stop()
