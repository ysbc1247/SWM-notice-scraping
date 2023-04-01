import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import requests
import time
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

# Set up email settings
FROM_EMAIL = 'ystc1247@gmail.com'
PASSWORD = 'kj10501050'
TO_EMAIL = 'ysbc1247@gmail.com'

# Set up scraping settings
URL = 'https://www.swmaestro.org/sw/mypage/mentoLec/list.do?menuNo=200046&searchStatMentolec=&hideAt=H&searchCnd=1&searchWrd=&pageIndex=1'
REFRESH_INTERVAL = 60 # seconds

# Define the index of the desired td element
index = 2

# Initialize the previous number to None
prev_number = None

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('client_secret_1087873534390-mik2p0h17fr0vs6692o4nl8vilbahse3.apps'
                                                 '.googleusercontent.com.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)
while True:
    # Make a GET request to the URL and extract the HTML content
    response = requests.get(URL, verify=False)
    html = response.text

    # Find the index of the nth occurrence of the "pc_only" class
    start_index = 0
    for i in range(index):
        start_index = html.find('class="pc_only">', start_index) + len('class="pc_only">')

    # Find the index of the closing </td> tag
    end_index = html.find('</td>', start_index)

    # Extract the number using string slicing
    number = html[start_index:end_index]

    # Check if the number has changed
    if prev_number is None or number != prev_number:
        # Construct the email message
        message = EmailMessage()
        message['To'] = TO_EMAIL
        message['Subject'] = 'New Mentoring Notification'

        # Send the email using Gmail's SMTP server
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(F'sent message to {message} Message Id: {message["id"]}')
        except HTTPError as error:
            print(F'An error occurred: {error}')
            message = None

        # Update the previous number
        prev_number = number
        print(prev_number)

    # Wait for the specified interval before checking again
    time.sleep(REFRESH_INTERVAL)
