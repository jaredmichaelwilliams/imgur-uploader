from imgurpython import ImgurClient

import click
import os
import datetime
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def get_config(plog):
    client_id = os.environ.get('IMGUR_API_ID')
    client_secret = os.environ.get('IMGUR_API_SECRET')

    config = ConfigParser.SafeConfigParser()
    config.read([os.path.expanduser('~/.config/imgur_uploader/uploader.cfg')])

    try:
        imgur = dict(config.items("imgur"))
    except:
        imgur = {}

    client_id = client_id or imgur.get("id")
    client_secret = client_secret or imgur.get("secret")
    access_token = imgur.get("access_token")
    refresh_token = imgur.get("refresh_token")

    if not (client_id and client_secret):
        return {}

    if (plog):
        return {"id": client_id, "secret": client_secret}

    if not (access_token and refresh_token):
        loginquestion = click.confirm("Not logged in. Do you want to login? Yes to login, No to upload anonymously",default=True,abort=False,prompt_suffix=': ',show_default=True)
        if (loginquestion == True):
            imgurlogin = imgur_login()
            return {"id": client_id, "secret": client_secret,"access_token": imgurlogin['access_token'],"refresh_token": imgurlogin['refresh_token']}
        else:
            return {"id": client_id, "secret": client_secret}

    return {"id": client_id, "secret": client_secret,"access_token": access_token,"refresh_token": refresh_token}


def imgur_login():
    """Logins to Imgur"""

    config = get_config(True)

    if not config:
        click.echo("Cannot upload - could not find IMGUR_API_ID or "
                   "IMGUR_API_SECRET environment variables or config file")
        return

    client = ImgurClient(config["id"], config["secret"])

    authorization_url = client.get_auth_url('pin')

    click.echo("Please Go To {}".format(authorization_url))

    login_pin = click.prompt('Please enter pin from the imgur login')

    credentials = client.authorize(login_pin,'pin')

    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    configvalues = ['access_token','refresh_token']

    for value in configvalues:
        with open(os.path.expanduser('~/.config/imgur_uploader/uploader.cfg')) as cf:
            lines = cf.readlines()
            ln = len(value)
            for ind, line in enumerate(lines):
                if value == line[:ln]:
                    lines[ind:ind+1] = []
                    break
            with open(os.path.expanduser('~/.config/imgur_uploader/uploader.cfg'),"w") as out:
                out.writelines(lines)

    with open(os.path.expanduser('~/.config/imgur_uploader/uploader.cfg'), "a") as cf:
	    cf.write("access_token=")
	    cf.write(credentials['access_token'])
	    cf.write("\nrefresh_token=")
	    cf.write(credentials['refresh_token'])

    return {"access_token": credentials['access_token'], "refresh_token": credentials['refresh_token']}

def get_details(userinput):
   defaulttitle = "Image on {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
   defaultdesc = "Uploaded by Jared.NYC's Imgur Uploader on {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

   if (userinput):
       title = click.prompt("Please enter a title", prompt_suffix=': ', show_default=False, default=defaulttitle)
       desc = click.prompt("Please enter a description", prompt_suffix=': ', show_default=False, default=defaultdesc)
       return{"title": title, "description": desc}
   else:
       return{"title": defaulttitle, "description": defaultdesc}


@click.command()
@click.option('image','--image', type=click.Path(exists=True))
@click.option('--login','login',is_flag=True,is_eager=True,help='Login To Imgur')
@click.option('--add-details','add_details',is_flag=True,help='Add a title and Description')
def upload_image(image,login,add_details):
    """Uploads an image file to Imgur"""

    if login:
        imgur_login()
        return

    if add_details:
        imagedetails = get_details(True)
    else:
        imagedetails = get_details(False)

    config = get_config(False)

    if not config:
        click.echo("Cannot upload - could not find IMGUR_API_ID or "
                   "IMGUR_API_SECRET environment variables or config file")
        return

    if not (config['access_token'] and config['refresh_token']):
        client = ImgurClient(config["id"], config["secret"])
        anonval = True
    else:
        client = ImgurClient(config["id"], config["secret"],config['access_token'],config['refresh_token'])
        anonval = False

    click.echo('Uploading file {}'.format(click.format_filename(image)))

    response = client.upload_from_path(image,config=imagedetails, anon=anonval)

    click.echo('File uploaded - see your image at {}'.format(response['link']))

    try:
        import pyperclip
        pyperclip.copy(response['link'])
    except ImportError:
        print("pyperclip not found. To enable clipboard functionality,"
              " please install it.")

if __name__ == '__main__':
    upload_image()
