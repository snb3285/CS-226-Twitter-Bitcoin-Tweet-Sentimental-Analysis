# CS-226-Twitter-Bitcoin-Tweet-Sentimental-Analysis
1. For implementation of sentiment analysis with Kaggle, we can see the instructions and run our code in “Sentiment_Analysis_Kaggle.ipynb” 
2. The code for preprocessing tweets from the Kaggle dataset is called BitcoinTweetProcessing.ipynb. It is run with Anaconda using Jupyter
Notebook. It is stored in the parent code directory. It takes in rows from the Kaggle Dataset of Bitcoin Tweets file tweets.csv and outputs the 
timestamp and preprocessed Tweet text for each row in the file preprocessed_tweets.csv, which is saved in the parent code directory. The
packages used to run this code are Anaconda3 2021.05, Python 3.8.8 64-bit, findspark 1.4.2, PySpark 3.2.0, nltk 3.6.1, textblob 0.15.3, Spark
3.2.0, OpenJDK 1.8.0_41, re, and os. re and os are built-in Python packages. To run PySpark correctly, follow the tutorial at
https://www.youtube.com/watch?v=DznteGdeJoA. To avoid possible errors, the path names for the Java and Spark installations should not
contain any whitespace.
3. To recover the modeling and prediction, we first need to do futher preprocessing of the tweet text and then combine with the Bitcoin price data which is named "coin_Bitcoin.csv" in the modeling_data folder, the result output file is named as "textblob_data.csv" in the modeling_data folder. The code to accompolish this is saved as "twitter_preprocessing.ipynb" in the modeling_code folder.
4. For implementation of linear model and Gradient Boosting model, refer to the "spark_ML_model.ipynb" in the modeling_code folder, and it also outputs a dataset named "lstmdata.csv" in the modeling_data folder for building the LSTM model.
5. For implementation of linear model and Gradient Boosting model, refer to the "LSTM_model.ipynb" in the modeling_code folder.
6. To visualize the code, open a terminal and navigate to the Visualization folder in this project. Run the application using ```python app.py``` and then go to your browser and enter ```localhost:5000```










####For the pipeline 

1. Open the folder SentimentalAnalysis and Run Driver.py for instantiating Listener Class 
2. Run senana.py for receiving tweets.  
The code for pipeline is present in SentimentalPipeline folder under the parent code directory and 
first you will have to run the driver.py to start the Tweet Listener Class. Once the class is started,
you can run senana.py to start retrieving data from twitter. The tweets will be saved in parquet files in parc directory in SentimentalPipeline folder. 
3. Run parquetparserpy to combine parquet scores.
