#Importing required modules
import mysql.connector
from datetime import datetime
import tweetle.packages.commands as commands 

#Establishing connection and creating cursor

class db():
    def __init__(self, user):
        sql_user = commands.Commands(user).read_accs()[4]
        pw = commands.Commands(user).read_accs()[5]
        self.mydb = mysql.connector.connect(host="localhost", user= sql_user,password=pw, port = 3306)
        mycursor = self.mydb.cursor(buffered=True)

        try:
            mycursor.execute("USE tweepy")
        except mysql.connector.Error as err:
            mycursor.execute("CREATE DATABASE tweepy")
            mycursor.execute("USE tweepy")

        try:
            mycursor.execute("SELECT * FROM TweetDB")
        except mysql.connector.Error as err:
            self.create()
        mycursor.close()

    #Table creation
    def create(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE Table TweetDB (SrlNo int NOT NULL AUTO_INCREMENT PRIMARY KEY, TweetID bigint, TweetTXT varchar(500), _Timestamp datetime, _URL varchar(10000), Author varchar(50))")

    #Data insertion
    def Insert_Data(self, TweetList):
        mycursor = self.mydb.cursor(buffered=True)
        insert_query = "INSERT INTO TweetDB (TweetID,TweetTXT,_Timestamp,_URL,Author) VALUES(%s,%s,%s,%s,%s)"
        records = (TweetList['id'], TweetList['tweet_text'], TweetList['timestamp'], TweetList['url'], TweetList['tweet_author'])
        mycursor.execute(insert_query, records)
        self.mydb.commit()
        mycursor.close()

    #Queries

    #Ordering by timestamp
    def orderbytime(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM TweetDB ORDER BY _Timestamp ASC")
        self.mydb.commit()
        res = mycursor.fetchall()
        mycursor.close()
        return res

    #Fetching top x rows
    def selecttop(self, x):
        mycursor = self.mydb.cursor(buffered=True)
        query = '''SELECT * FROM TweetDB
    LIMIT {}'''.format(x)
        mycursor.execute(query)
        self.mydb.commit()
        res = mycursor.fetchall()
        mycursor.close()
        return res

    #Emptying the whole table
    def clean(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("TRUNCATE TweetDB")
        self.mydb.commit()

    #Returning xth row
    def row(self, x):
        mycursor = self.mydb.cursor(buffered=True)
        query = '''SELECT * FROM TweetDB
    LIMIT {}'''.format(x)
        mycursor.execute(query)
        self.mydb.commit()
        res = mycursor.fetchall()
        res = res[len(res) - 1]
        mycursor.close()
        return res

    def all_data(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM TweetDB")
        res = mycursor.fetchall()
        mycursor.close()

        return res