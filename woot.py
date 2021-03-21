import requests
import os
import sys
import argparse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Get args from user
parser = argparse.ArgumentParser(description="Searches woot.com for offers")
parser.add_argument(
    "-e",
    "--email",
    help="email address to send results to",
    required=True
)
parser.add_argument(
    "-f",
    "--feed",
    help="Feed to query items from",
    choices=['All', 'Clearance', 'Computers', 'Electronics', 'Featured', 'Home', 'Gourmet', 'Shirts', 'Sports', 'Tools', 'Wootoff'],
    required=True
)
parser.add_argument(
    "-s",
    "--sub",
    help="Sub feed to filter. ex. Bedding for a search of Home/Bedding",
    required=False
)
parser.add_argument(
    "-c",
    "--criteria",
    help="Search criteia to filter results",
    required=False
)
args = vars(parser.parse_args())


def add_urls(data):

    # Creating an empty string for our html
    template = """"""

    for key in data:
        html = """\

               <li><a href="{}">{}</a></li>

        """.format(key, data[key])

        # Appending formatted html to template
        template+=html

    return template


# This function was found on https://realpython.com/python-send-email/
# and has only been modified slightly
def send_mail(link):

    sender_email = args['email']
    receiver_email = args['email']

    try:
        password = os.environ['EMAIL_KEY']
    except KeyError:
        print('Email key not found in environment variables')
        sys.exit(1)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Woot has what you are looking for!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,

    I've found the following item(s) on Woot that match your search!

    {}
    """.format(link)
    html = """\
    <html>
      <body>
        <p>Hi,</p>
        <p>I've found the following item(s) on Woot that match your search!</p>
        <ul>
            {}
        </ul>   
        <p>Thanks for using woot-notify!</p>
      </body>
    </html>
    """.format(link)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def main():

    api_base_url = "https://developer.woot.com/feed/"
    api_endpoint = args['feed']

    # Setting our search based on args provided
    # TODO: not all feeds return the feed name in upper case, i.e. electronics
    if args['sub']:
        item_filter = args['feed'].upper()+"/"+args['sub']
    else:
        item_filter = args['feed'].upper()

    try:
        key = os.environ['WOOT_KEY']
    except KeyError:
        print('API key not found in environment variables.')
        sys.exit(1)

    r = requests.get(api_base_url+api_endpoint, headers={"x-api-key": key})
    
    # Ensure our API request succeeded 
    if r.status_code != 200:
        print('GET failed with {}'.format(r.status_code)) 
        sys.exit(1)

    # Convert the response to a json object to make it easier to work with
    json_response = r.json()

    # Creating an empty dictionary for returned urls later
    urls = {}

    # Loop through the response
    # Add item titles and urls to our dictionary to email later 
    for item in json_response['Items']:
        if args['criteria']:
            if item_filter in item['Categories'] and item['IsSoldOut'] == False and args['criteria'] in item['Title']:
                urls[item['Url']] = item['Title']
        else:
            if item_filter in item['Categories'] and item['IsSoldOut'] == False:
                urls[item['Url']] = item['Title']
    
    # Email results matching our search criteria if present
    # TODO: Maybe track empty results in a log or something?
    if urls:
        search_results = add_urls(urls)
        send_mail(search_results)
    else: 
        pass

if __name__ == '__main__':
    main()