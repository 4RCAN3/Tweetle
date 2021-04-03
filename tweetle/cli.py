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




def about():
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


def commands():
    click.secho('''
-tweet: Use this command to tweet out anything. Usage: "-tweet Hi, I'm using tweetle"
-fetch: Use this command to store a number of tweets based on a keyword in a database. Usage: "-fetch Elon Musk 5"
-clean: Use this command to clean the database. Usage: "-clean"
-data: Use this command to get all the data stored in the database. Usage: "-data"
-row: Use this command to get data for a specifc row in the database. Usage: "-row 5"
-first: Use this command to get the earliest entries in the database. Usage: "-first 5"
-retweet: Use this command to retweet a particular row from the database. Usage: "-retweet 2"
-latest: Use this command to see the database arranged by time. Usage: "-latest"''', fg = 'bright_yellow')


def tweet(tw):
    '''This command tweets for you
Example usage: tweetle tweet Hi, I'm using tweetle'''

    tweet_obj = tweetObj()
    tweet_obj.tweet(' '.join(i for i in tw))
    click.secho('[+] Tweeted!', fg = 'bright_green')



def retweet(num):
    '''This command retweets the tweet for a specified row
Example usage: tweetle retweet 5 (This will retweet the tweet for the 5th row in the database)'''

    tweet_obj = tweetObj()

    id = ProjPySQL.row(int(num))[1]

    tweet_obj.retweet(int(id))

    click.secho('[+] Retweeted!', fg = 'bright_yellow')


def CleanDB():
    '''Truncates the database
Example usage: tweetle cleandb'''

    ProjPySQL.clean()
    click.secho('[-] The database is now cleaned!', fg = 'bright_red')


def fetch(name, num):
    '''Fetches a given amount of top tweets for a specific keyword and adds them to database
Example usage: tweetle fetch Elon Musk 3'''

    tweet_obj = tweetObj()
    tweets = tweet_obj.fetch(' '.join(i for i in name), int(num))
    for tweet in tweets:
        tweet_data = {'id' : tweet.id, 'tweet_text' : tweet.text, 'timestamp' : (tweet.created_at).strftime("%Y-%m-%d %H:%M:%S"), 'url' : f'https://twitter.com/twitter/statuses/{tweet.id}', 'tweet_author' : tweet.author.name}
        ProjPySQL.Insert_Data(tweet_data)
    
    click.secho(f'[+] Added {num} tweets to the database!', fg = 'bright_green')


def alldata():
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
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)


def getrow(num):
    '''A command to get a specific row
Example usage: tweetle getrow 3'''

    data = ProjPySQL.row(int(num))
    
    click.secho(f'''
Serial Number : {data[0]}
ID: {data[1]}
Tweet Text: {data[2]}
Timestamp: {data[3]}
Url: {data[4]}
Author: {data[5]}''', fg = 'bright_green')


def top(num):
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
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)


def bytime():
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
    
    table = PrettyTable(['Serial No.', 'Tweet ID', 'Tweet Text', 'Tweet Time', 'Tweet URL', 'Tweet Author'])

    for i in list_data:
        table.add_row(i)

    click.echo(table)



@click.command()
def cli():
    click.secho('''
$$$$$$$$\                                 $$\     $$\           
\__$$  __|                                $$ |    $$ |          
   $$ |$$\  $$\  $$\  $$$$$$\   $$$$$$\ $$$$$$\   $$ | $$$$$$\  
   $$ |$$ | $$ | $$ |$$  __$$\ $$  __$$\\_$$  _|  $$ |$$  __$$\ 
   $$ |$$ | $$ | $$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$ |$$$$$$$$ |
   $$ |$$ | $$ | $$ |$$   ____|$$   ____| $$ |$$\ $$ |$$   ____|
   $$ |\$$$$$\$$$$  |\$$$$$$$\ \$$$$$$$\  \$$$$  |$$ |\$$$$$$$\ 
   \__| \_____\____/  \_______| \_______|  \____/ \__| \_______|''',fg = 'bright_cyan')

    while True:
        click.echo('\n')
        click.secho('Looking for a user...', fg = 'bright_yellow')
        if os.environ.get('consumer_key') != None and os.environ.get('consumer_secret') and os.environ.get('access_token') != None and os.environ.get('access_token_secret') != None:
            
            click.secho('[+] User Found', fg = 'bright_green')
            break
        else:

            click.secho('[-] No user found', fg = 'bright_red')
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
            
            click.secho('[+] User Entered', fg = 'bright_blue')
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
        
        elif inp.startswith('-tweet'):
            status = inp.split(' ')[1:]
            click.echo(status)
            tweet(status)

        elif inp.startswith('-fetch'):
            num = inp.split(' ')[-1]
            keyword = inp.split(' ')[1:-1]
            fetch(keyword, int(num))

        elif inp.startswith('-clean'):
            CleanDB()
        
        elif inp.startswith('-retweet'):
            num = inp.split(' ')[1]
            retweet(int(num))

        elif inp.startswith('-data'):
            alldata()

        elif inp.startswith('-row'):
            num = inp.split(' ')[1]
            getrow(int(num))

        elif inp.startswith('-first'):
            num = inp.split(' ')[1]
            top(int(num))

        elif inp.startswith('-latest'):
            bytime()

        else:
            click.echo('Invalid Option')