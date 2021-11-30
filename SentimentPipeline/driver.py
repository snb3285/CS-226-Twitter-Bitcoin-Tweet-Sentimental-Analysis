"""
The class will be used to establish connection between Twitter and Spark Streaming via TCP Socket
TC: O(number of tweets received at an instant)
SC: O(number of rows in the parquet file)
"""
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import socket
import json
consumer_key='PqzQQUv1gjISqNQdQTwKoCCrU'
consumer_secret='DQgQOInJHcbKaD88eLBRIKR77Ifd4IbqPZnpXq7m2Q3EHZG2g4'
access_token ='712700196-mFwqTeMVxdDFzqpp2TsRxi400ET3X1zjYsuYTWgd'
access_secret='5HMIDEOV9Yp1TNN3fLoJ1vp7llpp7ACS6XBsJMTW7PtoR'
class ListenerClass(StreamListener):
    # tweet object listens for the tweets
    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            if "extended_tweet" not in msg:
                self.client_socket \
                    .send(str(msg['text'] + "t_end") \
                          .encode('utf-8'))
                print(msg['text'])
            else:
                self.client_socket \
                    .send(str(msg['extended_tweet']['full_text'] + "t_end") \
                          .encode('utf-8'))
                print(msg['extended_tweet']['full_text'])
            return True
        except BaseException as e:
            print("Exception")
        return True

    def on_error(self, status):
        print("The error status is", status)
        return True


def sendData(c_socket, keyword):
      print('Twitter to socket data sending begins')
      auth = OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_secret)
      twitter_stream = Stream(auth, ListenerClass(c_socket))
      twitter_stream.filter(track = keyword, languages=["en"])

if __name__ == "__main__":
        s = socket.socket()
        host = "0.0.0.0"
        port = 5555
        s.bind((host, port))
        print('Ready Socket')
        s.listen(4)
        print('Listening Socket')
        c_socket, addr = s.accept()
        print("Request received from: " + str(addr))
        sendData(c_socket, keyword = ['Bitcoin'])



