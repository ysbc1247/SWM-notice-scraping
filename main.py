import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import requests
import time

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
        message['From'] = FROM_EMAIL
        message['To'] = TO_EMAIL
        message['Subject'] = 'New Mentoring Notification'

        # Send the email using Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(FROM_EMAIL, PASSWORD)
            smtp.send_message(message)

        # Update the previous number
        prev_number = number

    # Wait for the specified interval before checking again
    time.sleep(REFRESH_INTERVAL)
