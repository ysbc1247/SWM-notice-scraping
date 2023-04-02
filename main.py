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

# Set the login URL and credentials
LOGIN_URL = 'https://www.swmaestro.org/sw/member/user/forLogin.do?menuNo=200025'
USERNAME = email
PASSWORD = pw

# Create a session object
session = requests.Session()

# Send a GET request to the login page to get any required CSRF tokens or cookies
response = session.get(LOGIN_URL, verify=False)
print(response.cookies.items())

# Extract the CSRF token from the response
csrf_token = response.text.split('name="csrfToken" id="csrfToken" value="')[1].split('"')[0]

# Set up the login data


# Set up email settings
FROM_EMAIL = 'ystc1247@gmail.com'
PASSWORD = pw
TO_EMAIL = 'ysbc1247@gmail.com'

# Set up scraping settings
URL = 'https://www.swmaestro.org/sw/mypage/mentoLec/list.do?menuNo=200046&searchStatMentolec=&hideAt=H&searchCnd=1&searchWrd=&pageIndex=1'
REFRESH_INTERVAL = 60 # seconds

# Define the index of the desired td element
index = 4

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
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrfToken': csrf_token
    }

    # Send a POST request to the login URL with the login data
    response = session.post(LOGIN_URL, data=login_data, verify=False)

    # Check if the login was successful
    if '로그인 실패' in response.text:
        print('Login failed')
    else:
        print('Login successful')
    # Make a GET request to the URL and extract the HTML content
    response = session.get(URL, verify=False)
    html = response.text

    # Find the index of the nth occurrence of the "pc_only" class
    start_index = 0
    for i in range(index):
        start_index = html.find('class="pc_only">', start_index) + len('class="pc_only">')
        end_index = html.find('</td>', start_index)
        number = html[start_index:end_index]
        print(number)

    # Find the index of the closing </td> tag


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
