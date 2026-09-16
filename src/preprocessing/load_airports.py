from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when

spark = SparkSession.builder \
    .appName("AirlineRouteBDA-Airports") \
    .getOrCreate()

input_path = "hdfs://localhost:9000/airline-route-bda/raw/airports.csv"
output_path = "data/processed/airports_clean"

airports = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(input_path)

# Replace \N with null
for c in airports.columns:
    airports = airports.withColumn(
        c,
        when(trim(col(c).cast("string")) == r"\N", None)
        .otherwise(col(c))
    )

# Remove duplicate airport records
airports = airports.dropDuplicates(["airport_id"])

# Convert numeric columns to proper numeric types
airports = airports \
    .withColumn("airport_id", col("airport_id").cast("integer")) \
    .withColumn("latitude", col("latitude").cast("double")) \
    .withColumn("longitude", col("longitude").cast("double")) \
    .withColumn("altitude", col("altitude").cast("integer"))

airports.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print("Airports preprocessing completed")
print("Total airports:", airports.count())

spark.stop()