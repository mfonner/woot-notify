import requests
import os
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#TODO: Args?

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

    sender_email = "matthewfonner@gmail.com"
    receiver_email = "matthewfonner@gmail.com"

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

    url = "https://developer.woot.com"
    feed_name = "/feed/home"

    try:
        key = os.environ['WOOT_KEY']
    except KeyError:
        print('API key not found in environment variables.')
        sys.exit(1)

    r = requests.get(url+feed_name, headers={"x-api-key": key})
    
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
        if "HOME/Bedding" in item['Categories'] and item['IsSoldOut'] == False:
            urls[item['Url']] = item['Title']
    
    # Email results matching our search criteria
    search_results = add_urls(urls)
    send_mail(search_results)

if __name__ == '__main__':
    main()