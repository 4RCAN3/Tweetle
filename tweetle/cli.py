try:
    import click
    import tweetle.packages.commands as commands
    import stdiomask
    from art import *
    import json
    import ascii_magic
    from ascii_graph import Pyasciigraph
    import colorama
    from ascii_graph.colordata import vcolor
    import sys
    from ascii_graph.colors import *
    import time

except Exception as e:
    print("Import Error", e)


__author__ = 'ARC4N3'
__email__ = 'arcaneisc00l@gmail.com'
__license__ = 'MIT'




def write():
    """
    A funtion to write the credentials of a user in a text file
    """    

    #Credentials will be identified from a username, it doesn't have to match the twitter username
    username = click.prompt("Enter a username (Doesn't have to match your twitter username, can be anything)")

    #getting the API keys and tokens
    api_key = click.prompt('Enter Your API Key')
    api_key_secret = click.prompt('Enter Your Api Key Secret')
    access_token = click.prompt('Enter Your Access Token')
    access_token_secret = click.prompt('Enter Your Access Token Secret')
    
    #Getting the SQL user and password
    sql_user = click.prompt('Enter your SQL user')
    pw = stdiomask.getpass('Enter your SQL password')
    click.secho('Setting up user', fg = 'bright_yellow')

    #The information is stored in a JSON format in the text file
    account_info = {username: {'Api_Key': api_key, 'Api_Secret': api_key_secret, 'Access_Token': access_token, 'Access_Token_Secret': access_token_secret, 'sql_user': sql_user, 'pass': pw}}

    with open("tweetle\packages\Accounts.txt", "a") as acc:
        account_info = json.dumps(account_info)
        acc.write(account_info + '\n')
        acc.close()

    click.secho('[+] Done setting up the user', fg = 'bright_blue')



@click.command()
def cli():

    """
    Entry Point for tweetle
    """    

    click.secho('''
$$$$$$$$\                                 $$\     $$\           
\__$$  __|                                $$ |    $$ |          
   $$ |$$\  $$\  $$\  $$$$$$\   $$$$$$\ $$$$$$\   $$ | $$$$$$\  
   $$ |$$ | $$ | $$ |$$  __$$\ $$  __$$\\_$$  _|  $$ |$$  __$$\ 
   $$ |$$ | $$ | $$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$ |$$$$$$$$ |
   $$ |$$ | $$ | $$ |$$   ____|$$   ____| $$ |$$\ $$ |$$   ____|
   $$ |\$$$$$\$$$$  |\$$$$$$$\ \$$$$$$$\  \$$$$  |$$ |\$$$$$$$\ 
   \__| \_____\____/  \_______| \_______|  \____/ \__| \_______|
   ''',fg = 'bright_cyan')

    #A setup for tweetle interface
    while True:

        #Checking if the user exists in the added accounts
        user = click.prompt('Enter Account User (Type "none" if not setup or if entering a new user)')
        if user.lower() != 'none':
            comm = commands.Commands(user)
            try:
                api_key, api_key_secret, access_token, access_token_secret, sql_username, sql_pw = comm.read_accs()
                import tweetle.packages.ProjPySQL as ProjPySQL
                sql = ProjPySQL.db(user)
                click.secho('[+] User Found', fg = 'bright_green')

                break
            
            except Exception as e:
                print(e)
                click.secho('[-] Invalid User, Try Again.', fg = 'bright_red')

        #If the user wants to setup a new account
        else:
            write()
    
    #User's profile information
    me = comm.profile()
    my_user = me.name
    my_desc = me.description
    followers = int(me.followers_count)
    following = int(me.friends_count)
    created = me.created_at
    status_count = int(me.statuses_count)
    prof_image = me.profile_image_url
    prof_banner = me.profile_banner_url

    #Stats bar
    stats = [('Followers', followers), ('Following', following), ('Tweets', status_count)]
    pattern = [Gre, Yel, Red]
    data = vcolor(stats, pattern)

    #Welcome art
    welcome = text2art('Welcome' + '  ' + my_user)
    
    #Welcome animation
    colorama.init(autoreset = False)
    click.echo('\n')
    for letter in welcome:
        sys.stdout.write(colorama.Fore.CYAN)
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.000075)

    click.echo('\n')

    #Your stats animation
    your_stats = text2art('YOUR STATS')
    for letter in your_stats:
        sys.stdout.write(colorama.Fore.LIGHTRED_EX)
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.0000075)

    graph = Pyasciigraph()

    #Statistics animation
    for line in  graph.graph(f'Description: {my_desc}', data)[2:]:
        for letter in line:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.02)
        print('\n')


    #Command prompts
    while True:
        click.echo('\n')
        inp = click.prompt('Tweetle')


        if inp.lower() == '-a':
            comm.about()

        elif inp.lower == '-o':
            click.echo('''
OPTIONS:
-a : About Tweetle
-c : Get a list of commands
-v : Get the version
-q : Quit''')

        elif inp.lower() == '-q':
            break

        elif inp.lower() == '-c':
            comm.commands()
        
        elif inp.startswith('-tweet'):
            status = inp.split(' ')[1:]
            click.echo(status)
            comm.tweet(status)

        elif inp.startswith('-fetch'):
            num = inp.split(' ')[-1]
            keyword = inp.split(' ')[1:-1]
            comm.fetch(sql, keyword, int(num))

        elif inp.startswith('-clean'):
            comm.CleanDB(sql)
        
        elif inp.startswith('-retweet'):
            num = inp.split(' ')[1]
            comm.retweet(sql, int(num))

        elif inp.startswith('-data'):
            comm.alldata(sql)

        elif inp.startswith('-row'):
            num = inp.split(' ')[1]
            comm.getrow(sql, int(num))

        elif inp.startswith('-first'):
            num = inp.split(' ')[1]
            comm.top(sql, int(num))

        elif inp.startswith('-latest'):
            comm.bytime(sql)

        else:
            click.echo('Invalid Option')


"""
Tweetle
ARC4N3, 2021
"""