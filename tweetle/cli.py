import click
import main_script
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

    twitter = main_script.Twitter(consumer_key, consumer_secret, access_token, access_token_secret)

    return twitter

@click.group()
def cli():
    '''Welcome to Tweetle. 
A CLI Made to control your twitter account and save information through your command line.
'''
    
    pass

@cli.command()
@click.argument('tw', nargs = -1)
def tweet(tw):
    '''This command tweets for you
Example usage: tweetle tweet Hi, I'm using tweetle'''

    tweet_obj = tweetObj()
    tweet_obj.tweet(' '.join(i for i in tw))
    click.echo('Tweeted!')

@cli.command()
@click.argument('num', nargs = 1)
def retweet(num):
    '''This command retweets the tweet for a specified row
Example usage: tweetle retweet 5 (This will retweet the tweet for the 5th row in the database)'''

    tweet_obj = tweetObj()

    id = ProjPySQL.row(int(num))[1]

    tweet_obj.retweet(int(id))

    click.echo('Retweeted!')

@cli.command()
def CleanDB():
    '''Truncates the database
Example usage: tweetle cleandb'''

    ProjPySQL.clean()
    click.echo('The database is now cleaned!')

@cli.command()
@click.argument('name', nargs = -1)
@click.argument('num', nargs = 1)
def fetch(name, num):
    '''Fetches a given amount of top tweets for a specific keyword and adds them to database
Example usage: tweetle fetch Elon Musk 3'''

    tweet_obj = tweetObj()
    tweets = tweet_obj.fetch(' '.join(i for i in name), int(num))
    for tweet in tweets:
        tweet_data = {'id' : tweet.id, 'tweet_text' : tweet.text, 'timestamp' : (tweet.created_at).strftime("%Y-%m-%d %H:%M:%S"), 'url' : f'https://twitter.com/twitter/statuses/{tweet.id}', 'tweet_author' : tweet.author.name}
        ProjPySQL.Insert_Data(tweet_data)
    
    click.echo(f'Added {num} tweets to the database!')


@cli.command()
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

@cli.command()
@click.argument('num', nargs = 1)
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

@cli.command()
@click.argument('num', nargs = 1)
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

@cli.command()
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
