import click
import tweetle.packages.tweefeed as tweefeed
import os
from dotenv import load_dotenv
from prettytable import PrettyTable
import stdiomask
import json


class Commands():
    
    
    def __init__(self, user):
        """[__init__]

        Args:
            user (str): [Account user for tweetle]
        """        
        self.user = user

    
    def profile(self):
        
        return self.tweetObj().prof()
        

    def read_accs(self):
        """[Reads The Accounts.txt file to get the user]

        Returns:
            [Tuple]: [Api key, Api key secret, Access token, Access token secret, SQL user, SQL pass]
        """        
        with open("tweetle\packages\Accounts.txt") as acc:
            choose_user = self.user
            users = acc.readlines()
            #Checking the user
            for user in users:
                user.replace("\n", "")
                user = json.loads(user)


                if choose_user in user:
                    key = user[choose_user]['Api_Key']
                    key_secret = user[choose_user]['Api_Secret']
                    token = user[choose_user]['Access_Token']
                    token_secret = user[choose_user]['Access_Token_Secret']
                    sql_user = user[choose_user]['sql_user']
                    sql_pass = user[choose_user]['pass']

                    return (key, key_secret, token, token_secret, sql_user, sql_pass)

            
            return None


    def tweetObj(self):
        """[Get the Twitter object]

        Returns:
            [object]: [Twitter object from tweefeed.py]
        """        
        consumer_key, consumer_secret, access_token, access_token_secret, sql_user, sql_pass = self.read_accs()
        twitter = tweefeed.Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

        return twitter
    
    
    def about(self):
        click.secho('''
Tweetle is a cli made by ARC4N3 to control                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Your twitter account through your cmd line                          @@@@@@@@@@@@@@@@@@@@@@@@/    , ,. &.@@@@@@@@@@@@@@@@@@@@@@@@@@
                                                                    @@@@@@@@@@@@@@@@@@@@&* .@@@@@@@@@@@   (@@@@@@@@@@@@@@@@@@@@@@@
Authors:                                                            @@@@@@@@@@@@@@@@@@@@, ##@  &@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@
ARC4N3 - Initial Work (https://github.com/4RCAN3/)                  @@@@@@@@@@@@@@@@  @   @@@@@@@@(./@@@@@   @@@@@@@@@@@@@@@@@@@@@
BlaZe - MySQL (https://github.com/BlaZeSama)                        @@@@@@@@@@@@@@@@     @@@@@@   @@@. .@@   @@@@@@@@@@@@@@@@@@@@@
                                                                    @@@@@@@@@@@@@@@@@@#  @@@@@, .@@@@@@*      @@@@@@@@@@@@@@@@@@@@
                                                                    @@@@@@@@@@@@@@@@@@@  @@@@@, @@@@@@@@@     @@@@@@@@@@@@@@@@@@@@
License: MIT                                                        @@@@@@@@@@@@@@@@@@@@  .@@@@  /@@@@@@@@@    &@@@@@@@@@@@@@@@@@@
https://github.com/4RCAN3/Tweetle/blob/master/LICENSE               @@@@@@@@@@@@@@@@@@@@&  /@@@.  @@@@@@@@ /   .@@@@@@@@@@@@@@@@@@
                                                                    @@@@@@@@@@@@@@@@@@@@@*   @@@ @ @@@@@@ @     @@@@@@@@@@@@@@@@@@
Contribute:                                                         @@@@@@@@@@@@@@@@@@@@@@@   /@@%@ @@@# % ,    @@@@@@@@@@@@@@@@@@
https://github.com/4RCAN3/Tweetle                                   @@@@@@@@@@@@@@@@@@@@@@@@ *  @.( @,         @@@@@@@@@@@@@@@@@@@
                                                                    @@@@@@@@@@@@@@@@@@@@@@@@@@%      , , # ..  @@@@@@@@@@@@@@@@@@@
Support us by buying us a coffee :)                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*        %@@@@@@@@@@@@@@@@@@@@
https://ko-fi.com/arc4n3                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@''', fg = 'bright_green')


    def commands(self):
        click.secho('''
-tweet: Use this command to tweet out anything. Usage: "-tweet Hi, I'm using tweetle"
-fetch: Use this command to store a number of tweets based on a keyword in a database. Usage: "-fetch Elon Musk 5"
-clean: Use this command to clean the database. Usage: "-clean"
-data: Use this command to get all the data stored in the database. Usage: "-data"
-row: Use this command to get data for a specifc row in the database. Usage: "-row 5"
-first: Use this command to get the earliest entries in the database. Usage: "-first 5"
-retweet: Use this command to retweet a particular row from the database. Usage: "-retweet 2"
-latest: Use this command to see the database arranged by time. Usage: "-latest"''', fg = 'bright_yellow')


    def tweet(self, tw):
        '''This command tweets for you
Example usage: tweetle tweet Hi, I'm using tweetle'''

        tweet_obj = self.tweetObj()
        tweet_obj.tweet(' '.join(i for i in tw))
        click.secho('[+] Tweeted!', fg = 'bright_green')



    def retweet(self, ProjPySQL,  num):
        '''This command retweets the tweet for a specified row
Example usage: tweetle retweet 5 (This will retweet the tweet for the 5th row in the database)'''

        tweet_obj = self.tweetObj()
        id = ProjPySQL.row(int(num))[1]
        tweet_obj.retweet(int(id))

        click.secho('[+] Retweeted!', fg = 'bright_yellow')


    def CleanDB(self, ProjPySQL):
        '''Truncates the database
Example usage: tweetle cleandb'''

        ProjPySQL.clean()
        click.secho('[-] The database is now cleaned!', fg = 'bright_red')


    def fetch(self, ProjPySQL, name, num):
        '''Fetches a given amount of top tweets for a specific keyword and adds them to database
Example usage: tweetle fetch Elon Musk 3'''

        tweet_obj = self.tweetObj()
        tweets = tweet_obj.fetch(' '.join(i for i in name), int(num))
        for tweet in tweets:
            tweet_data = {'id' : tweet.id, 'tweet_text' : tweet.full_text, 'timestamp' : (tweet.created_at).strftime("%Y-%m-%d %H:%M:%S"), 'url' : f'https://twitter.com/twitter/statuses/{tweet.id}', 'tweet_author' : tweet.author.name}
            ProjPySQL.Insert_Data(tweet_data, ' '.join(i for i in name))
        
        click.secho(f'[+] Added {num} tweets to the database!', fg = 'bright_green')


    def alldata(self, ProjPySQL):
        '''A command to get all the data from the database
Example usage: tweetle alldata'''
        
        click.secho('Fetching data', fg = 'bright_yellow')

        data = ProjPySQL.all_data()
        list_data = []
        for row in data:
            temp_list = []
            for i in row:
                temp_list.append(i)
            list_data.append(temp_list)
        
        table = PrettyTable(['Serial No.', 'Tweet ID', 'Keyword', 'Tweet Time', 'Tweet Author'])

        for i in list_data:
            table.add_row(i)

        click.echo(table)


    def getrow(self, ProjPySQL, num):
        '''A command to get a specific row
Example usage: tweetle getrow 3'''

        data = ProjPySQL.row(int(num))

        try:
            tweet_text = self.tweetObj().get_tweet(data[1]).full_text
        except:
            tweet_text = self.tweetObj().get_tweet(data[1]).text

        
        click.secho(f'''
{tweet_text}

{data[3]}  -- by: {data[4]}

Find the tweet at: https://twitter.com/twitter/statuses/{data[1]}
Keyword Used: {data[2]}''', fg = 'bright_green')


    def top(self, ProjPySQL, num):
        '''A command to get a specific number of top rows from the database
Example usage: tweetle top 5'''

        click.secho(f'Fetching the first {num} rows', fg = 'bright_yellow')

        data = ProjPySQL.selecttop(int(num))
        list_data = []
        for row in data:
            temp_list = []
            for i in row:
                temp_list.append(i)
            list_data.append(temp_list)
        
        table = PrettyTable(['Serial No.', 'Tweet ID', 'Keyword', 'Tweet Time', 'Tweet Author'])

        for i in list_data:
            table.add_row(i)

        click.echo(table)


    def bytime(self, ProjPySQL):
        '''A command to get rows according to their timestamps (Latest first)
Example usage: tweetle order'''
        
        click.secho('Arranging the data according to timestamps.', fg = 'bright_yellow')
        data = ProjPySQL.orderbytime()

        list_data = []
        for row in data:
            temp_list = []
            for i in row:
                temp_list.append(i)
            list_data.append(temp_list)
        
        table = PrettyTable(['Serial No.', 'Tweet ID', 'Keyword', 'Tweet Time', 'Tweet Author'])

        for i in list_data:
            table.add_row(i)

        click.echo(table)