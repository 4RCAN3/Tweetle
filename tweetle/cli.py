import click
import tweefeed
import os
from dotenv import load_dotenv
import ProjPySQL
from prettytable import PrettyTable 


__author__ = 'ARC4N3'

def tweetObj():
    load_dotenv()

    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')
    access_token = os.environ.get('access_token')
    access_token_secret = os.environ.get('access_token_secret')
    twitter = tweefeed.Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

    return twitter


@click.command()
def cli():
    click.secho('''

████████ ██     ██ ███████ ███████ ████████ ██      ███████ 
   ██    ██     ██ ██      ██         ██    ██      ██      
   ██    ██  █  ██ █████   █████      ██    ██      █████   
   ██    ██ ███ ██ ██      ██         ██    ██      ██      
   ██     ███ ███  ███████ ███████    ██    ███████ ███████ 
                                                            
                                                            ''',fg = 'green')

    while True:
        '''consumer_key=C1gXCLn6fITSUb6uqFot9XYgl
consumer_secret=seLZWqSX1jI1bn1PbWcHvA55jbqIYc1VLxmDuXbQwnp9c5r7Rm
access_token=1140147595408363521-VVAya7SNuzuqFyhQI1y2wxiNBQXEZD
access_token_secret=VRcsRp6s7idjGD1BrVbaOYMv3Cm6hdM2CkmUOlNhczUx0'''
        click.secho('Looking for a user...', fg = 'yellow')
        if os.environ.get('consumer_key') != None and os.environ.get('consumer_secret') and os.environ.get('access_token') != None and os.environ.get('access_token_secret') != None:
            
            click.secho('[+] User Found', fg = 'green')
            break
        else:

            click.secho('[-] No user found', fg = 'red')
            api_key = click.prompt('Enter Your API Key')
            api_key_secret = click.prompt('Enter Your Api Key Secret')
            access_token = click.prompt('Enter Your Access Token')
            access_token_secret = click.prompt('Enter Your Access Token Secret')
            with open('.env', 'a') as fi:
                fi.write(f"\nconsumer_key={api_key}")
                fi.write(f"\nconsumer_secret={api_key_secret}")
                fi.write(f"\naccess_token={access_token}")
                fi.write(f"\naccess_token_secret={access_token_secret}")
                fi.close()
            
            click.secho('[+] User Entered', fg = 'blue')
            break
    
    click.echo('''
OPTIONS:
-a : About Tweetle
-c : Get a list of commands
-v : Get the version
-q : Quit''')
    while True:
        click.echo('\n')
        inp = click.prompt('Tweetle')

        if inp.lower() == '-a':
            about()
        elif inp.lower() == '-q':
            break
        elif inp.lower() == '-c':
            commands()
        else:
            click.echo('Invalid Option')


def about():
    click.secho('''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@/    , ,. &.@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@&* .@@@@@@@@@@@   (@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@, ##@  &@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@  @   @@@@@@@@(./@@@@@   @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@     @@@@@@   @@@. .@@   @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@#  @@@@@, .@@@@@@*      @@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@  @@@@@, @@@@@@@@@     @@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@  .@@@@  /@@@@@@@@@    &@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@&  /@@@.  @@@@@@@@ /   .@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@*   @@@ @ @@@@@@ @     @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@   /@@%@ @@@# % ,    @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@ *  @.( @,         @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@%      , , # ..  @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*        %@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@''', fg = 'blue')


def commands():
    click.secho('''
-tweet: Use this command to tweet out anything. Usage: "-tweet Hi, I'm using tweetle"
-fetch: Use this command to store a number of tweets based on a keyword in a database. Usage: "-fetch Elon Musk 5"
-clean: Use this command to clean the database. Usage: "-clean"
-data: Use this command to get all the data stored in the database. Usage: "-data"
-row: Use this command to get data for a specifc row in the database. Usage: "-row 5"
-first: Use this command to get the earliest entries in the database. Usage: "-first 5"
-retweet: Use this command to retweet a particular row from the database. Usage: "-retweet 2"
-latest: Use this command to see the database arranged by time. Usage: "-latest"''', fg = 'yellow')


def tweet(tw):
    '''This command tweets for you
Example usage: tweetle tweet Hi, I'm using tweetle'''

    tweet_obj = tweetObj()
    tweet_obj.tweet(' '.join(i for i in tw))
    click.echo('Tweeted!')



def retweet(num):
    '''This command retweets the tweet for a specified row
Example usage: tweetle retweet 5 (This will retweet the tweet for the 5th row in the database)'''

    tweet_obj = tweetObj()

    id = ProjPySQL.row(int(num))[1]

    tweet_obj.retweet(int(id))

    click.echo('Retweeted!')


def CleanDB():
    '''Truncates the database
Example usage: tweetle cleandb'''

    ProjPySQL.clean()
    click.echo('The database is now cleaned!')


def fetch(name, num):
    '''Fetches a given amount of top tweets for a specific keyword and adds them to database
Example usage: tweetle fetch Elon Musk 3'''

    tweet_obj = tweetObj()
    tweets = tweet_obj.fetch(' '.join(i for i in name), int(num))
    for tweet in tweets:
        tweet_data = {'id' : tweet.id, 'tweet_text' : tweet.text, 'timestamp' : (tweet.created_at).strftime("%Y-%m-%d %H:%M:%S"), 'url' : f'https://twitter.com/twitter/statuses/{tweet.id}', 'tweet_author' : tweet.author.name}
        ProjPySQL.Insert_Data(tweet_data)
    
    click.echo(f'Added {num} tweets to the database!')


def alldata():
    '''A command to get all the data from the database
Example usage: tweetle alldata'''

    data = ProjPySQL.all_data()
    list_data = []
    for row in data:
        temp_list = []
        for i in row:
            temp_list.append(i)
        list_data.append(temp_list)
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)


def getrow(num):
    '''A command to get a specific row
Example usage: tweetle getrow 3'''

    data = ProjPySQL.row(int(num))
    
    click.echo(f'''
Serial Number : {data[0]}
ID: {data[1]}
Tweet Text: {data[2]}
Timestamp: {data[3]}
Url: {data[4]}
Author: {data[5]}''')


def top(num):
    '''A command to get a specific number of top rows from the database
Example usage: tweetle top 5'''

    data = ProjPySQL.selecttop(int(num))
    list_data = []
    for row in data:
        temp_list = []
        for i in row:
            temp_list.append(i)
        list_data.append(temp_list)
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)


def bytime():
    '''A command to get rows according to their timestamps (Latest first)
Example usage: tweetle order'''

    data = ProjPySQL.orderbytime()

    list_data = []
    for row in data:
        temp_list = []
        for i in row:
            temp_list.append(i)
        list_data.append(temp_list)
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)
