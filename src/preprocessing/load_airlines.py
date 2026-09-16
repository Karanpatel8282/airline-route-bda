from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when

spark = SparkSession.builder \
    .appName("AirlineRouteBDA-Airlines") \
    .getOrCreate()

input_path = "hdfs://localhost:9000/airline-route-bda/raw/airlines.csv"
output_path = "data/processed/airlines_clean"

airlines = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(input_path)

# Replace \N with null
for c in airlines.columns:
    airlines = airlines.withColumn(
        c,
        when(trim(col(c).cast("string")) == r"\N", None)
        .otherwise(col(c))
    )

# Convert airline ID to integer
airlines = airlines.withColumn(
    "airline_id",
    col("airline_id").cast("integer")
)

# Remove duplicate airline records
airlines = airlines.dropDuplicates(["airline_id"])

airlines.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print("Airlines preprocessing completed")
print("Total airlines:", airlines.count())

spark.stop()