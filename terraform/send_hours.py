import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

#TODO lisää tuntien ja vastaanottajan haku sql instanssista

#Lahetetaan viesti
load_dotenv()

USERNAME = os.getenv('USERNAME_POSTI')
PASSWORD = os.getenv('PASSWORD_POSTI')
SENDER = os.getenv('SENDER_POSTI')
RECEIVER = os.getenv('RECEIVER_POSTI')

server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.ehlo()

server.login(USERNAME, PASSWORD)

fromaddr = SENDER 
toaddr = RECEIVER 
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Tuntikirjauksesi!"

body = "Hello World! Näin monta tuntia tulit tehneeksi:"
msg.attach(MIMEText(body, 'plain'))

text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)