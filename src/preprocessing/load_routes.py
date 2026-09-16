from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when

spark = SparkSession.builder \
    .appName("AirlineRouteBDA-Routes") \
    .getOrCreate()

input_path = "hdfs://localhost:9000/airline-route-bda/raw/routes.csv"
output_path = "data/processed/routes_clean"

routes = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(input_path)

# Replace \N with null
for c in routes.columns:
    routes = routes.withColumn(
        c,
        when(trim(col(c).cast("string")) == r"\N", None)
        .otherwise(col(c))
    )

# Convert numeric columns
routes = routes \
    .withColumn("airline_id", col("airline_id").cast("integer")) \
    .withColumn("source_airport_id", col("source_airport_id").cast("integer")) \
    .withColumn("destination_airport_id", col("destination_airport_id").cast("integer")) \
    .withColumn("stops", col("stops").cast("integer"))

# Remove duplicate routes
routes = routes.dropDuplicates([
    "airline_id",
    "source_airport_id",
    "destination_airport_id"
])

routes.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print("Routes preprocessing completed")
print("Total routes:", routes.count())

spark.stop()