# CS-226-Twitter-Bitcoin-Tweet-Sentimental-Analysis
1. For implementation of sentiment analysis with Kaggle, we can see the instructions and run our code in “Sentiment_Analysis_Kaggle.ipynb” 
2. To recover the modeling and prediction, we first need to do futher preprocessing of the text and then combine with the Bitcoin price data. For implementation of linear model and Gradient Boosting model, refer to the "spark_ML_model.ipynb"
3. 
4. For Neil










####For the pipeline 

1. Open the folder SentimentalAnalysis and Run Driver.py for instantiating Listener Class 
2. Run senana.py for receiving tweets.  
The code for pipeline is present in SentimentalPipeline folder under the parent code directory and 
first you will have to run the driver.py to start the Tweet Listener Class. Once the class is started,
you can run senana.py to start retrieving data from twitter. The tweets will be saved in parquet files in parc directory in SentimentalPipeline folder. 
3. Run parquetparserpy to combine parquet scores.
