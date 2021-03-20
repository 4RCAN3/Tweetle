#Importing required modules
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

#Establishing connection and creating cursor
mydb = mysql.connector.connect(host="localhost",database = 'tweepy', user= os.environ.get('user'),password=os.environ.get('pass'), port = 3306)

#Table creation
def create():
    mycursor = mydb.cursor()
    mycursor.execute("CREATE Table TweetDB (SrlNo int NOT NULL AUTO_INCREMENT PRIMARY KEY, TweetID bigint, TweetTXT varchar(500), _Timestamp datetime, _URL varchar(10000), Author varchar(50))")

#Data insertion
def Insert_Data(TweetList):
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO TweetDB (TweetID,TweetTXT,_Timestamp,_URL,Author) VALUES(%s,%s,%s,%s,%s)"
    records = (TweetList['id'], TweetList['tweet_text'], TweetList['timestamp'], TweetList['url'], TweetList['tweet_author'])
    mycursor.execute(insert_query, records)
    mydb.commit()
    mycursor.close()

#Queries

#Ordering by timestamp
def orderbytime():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM TweetDB ORDER BY _Timestamp ASC")
    mydb.commit()
    res = mycursor.fetchall()
    mycursor.close()
    return res

#Fetching top x rows
def selecttop(x):
    mycursor = mydb.cursor(buffered=True)
    query = '''SELECT * FROM TweetDB
LIMIT {}'''.format(x)
    mycursor.execute(query)
    mydb.commit()
    res = mycursor.fetchall()
    mycursor.close()
    return res

#Emptying the whole table
def clean():
    mycursor = mydb.cursor()
    mycursor.execute("TRUNCATE TweetDB")
    mydb.commit()

#Returning xth row
def row(x):
    mycursor = mydb.cursor(buffered=True)
    query = '''SELECT * FROM TweetDB
LIMIT {}'''.format(x)
    mycursor.execute(query)
    mydb.commit()
    res = mycursor.fetchall()
    res = res[len(res) - 1]
    mycursor.close()
    return res

def all_data():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM TweetDB")
    res = mycursor.fetchall()
    mycursor.close()

    return res