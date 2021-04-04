import click
import tweetle.packages.commands as commands
import stdiomask
import json

__author__ = 'ARC4N3'
__email__ = 'arcaneisc00l@gmail.com'
__license__ = 'MIT'

def write():
    username = click.prompt("Enter a username (Doesn't have to match your twitter username, can be anything)")

    api_key = click.prompt('Enter Your API Key')
    api_key_secret = click.prompt('Enter Your Api Key Secret')
    access_token = click.prompt('Enter Your Access Token')
    access_token_secret = click.prompt('Enter Your Access Token Secret')

    sql_user = click.prompt('Enter your SQL user')
    pw = stdiomask.getpass('Enter your SQL password')
    click.secho('Setting up user', fg = 'bright_yellow')

    account_info = {username: {'Api_Key': api_key, 'Api_Secret': api_key_secret, 'Access_Token': access_token, 'Access_Token_Secret': access_token_secret, 'sql_user': sql_user, 'pass': pw}}

    with open("tweetle\Accounts.txt", "a") as acc:
        account_info = json.dumps(account_info)
        acc.write(account_info + '\n')
        acc.close()

    click.secho('[+] Done setting up the user', fg = 'bright_blue')


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
   \__| \_____\____/  \_______| \_______|  \____/ \__| \_______|
   ''',fg = 'bright_cyan')

    while True:
        user = click.prompt('Enter Account User (Type "none" if not setup or if entering a new user)')
        if user.lower() != 'none':
            comm = commands.Commands(user)
            try:
                api_key, api_key_secret, access_token, access_token_secret, sql_username, sql_pw = comm.read_accs()
                import ProjPySQL
                sql = ProjPySQL.db(user)
                click.secho('[+] User Found', fg = 'bright_green')

                break
            except Exception as e:
                click.secho('[-] Invalid User, Try Again.', fg = 'bright_red')

        else:
            write()

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
            comm.about()

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