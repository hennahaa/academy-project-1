import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

#nämä salaisuudet määritellään .env filussa
USERNAME = os.getenv('USERNAME_POSTI')
PASSWORD = os.getenv('PASSWORD_POSTI')
SENDER = os.getenv('SENDER_POSTI')
RECEIVER = os.getenv('RECEIVER_POSTI')

#hakee dataa sql-kannsta, generoi viestin sähköpostille
#returns a message string 
def get_data():
    pass

def send_email():
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
    msg['Subject'] = "Tämä on testi!"

    #tää pitäis toimia loppuversiossa
    #body = get_data()
    body = 'Hello World!'
    
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)


#emailin lähetyksen suoritus
send_email()