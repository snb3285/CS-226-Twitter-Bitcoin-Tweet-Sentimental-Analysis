"""
This program will make a Spark Session and start reading the Tweets through Twitter Api via the Listener Class that should be run before running this program.
This program will Read through the tweets and do some very basic preprocessing to reflect the Tweet Sentiment Score of the tweets in an almost Real- Time manner.
We save the tweets and their scores in Parquet files. For modelling we won't use these results, we will use  Kaggle Dataset of 16M tweets which is more encompassive and we feel
should yield more accurate results in modelling. As was taught in coursework, we observed Streaming Pipeline does not give related tweets all the time and we need to save those tweets somewhere before pre-processing.
Time Complexity: O(linear size of input)
Space Complexity: O(~size of input)

"""

from textblob import TextBlob
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.sql.types import *

def preprocessing(rows):
    stringWords = rows.select(explode(split(rows.value, "t_end")).alias("word"))
    ###Splitting the tweet by t_end and storing in list
    stringWords = stringWords.na.replace('', None)
    ###Replacing blanks with null
    stringWords = stringWords.na.drop()
    ###And then deleting those nulls
    """Doing basic pre-processing"""
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', r'http\S+', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', '@\w+', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', '#', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', 'RT', ''))
    stringWords = stringWords.withColumn('word', functions.regexp_replace('word', ':', ''))
    return stringWords

"""
Basic Sentence Classification polarity and subjectivity below
To be explained in depth in Hsi-Min's part
"""
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
    ##We create a spark session
    rows = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    ###reading each row storing in list(rows)
    stringWords = preprocessing(rows)
    ###We preprocess each row and pass through vader
    stringWords = text_classification(stringWords)
    stringWords = stringWords.repartition(1)
    ###We output the results in parquet file
    query = stringWords.writeStream.queryName("all_tweets")\
        .outputMode("append").format("parquet")\
        .option("path", "./parc")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='60 seconds').start()
    query.awaitTermination()