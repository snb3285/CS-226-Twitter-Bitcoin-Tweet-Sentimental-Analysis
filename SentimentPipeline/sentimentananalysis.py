"""
TC: O(linear size of input)
SC: O(~size of input)
"""

from textblob import TextBlob
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.sql.types import *

def preprocessing(rows):
    stringWords = rows.select(explode(split(rows.value, "t_end")).alias("word"))
    stringWords = stringWords.na.replace('', None)
    stringWords = stringWords.na.drop()
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', r'http\S+', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', '@\w+', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', '#', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', 'RT', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', ':', ''))
    return stringWords

"""Sentence Classification polarity and subjectivity below"""
def polarity_detection(sentence):
    return TextBlob(sentence).sentiment.polarity

def subjectivity_detection(sentence):
    return TextBlob(sentence).sentiment.subjectivity

def text_classification(stringWords):
    polarity_detection_udf = udf(polarity_detection, StringType())
    stringWords = stringWords.withColumn("polarity", polarity_detection_udf("word"))
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    stringWords = stringWords.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return stringWords

"""Driver Code"""
if __name__ == "__main__":
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()
    rows = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    stringWords = preprocessing(rows)
    stringWords = text_classification(stringWords)
    stringWords = stringWords.repartition(1)
    query = stringWords.writeStream.queryName("all_tweets")\
        .outputMode("append").format("parquet")\
        .option("path", "./parc")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='60 seconds').start()
    query.awaitTermination()