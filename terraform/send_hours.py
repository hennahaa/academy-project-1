import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

#KOVAKOODATTUA TESTIJUTTUA ALLA, POISTA LOPUKSI

#TODO lisää tuntien ja vastaanottajan haku sql instanssista
#kovakoodattua mockkitietoa
start_date  = "24-12-2021"
start_time = "07:42"
end_date  = "24-12-2021"
end_time = "16:12"
assignment = "Tunkkausta"
weather = "Snowy"
#project_id = 3
#user_id = 2
#ID:den avulla tehdään SQL kysely jolla saadaan tauluista nimet
project_name = "Ylläpitopainajainen"
user_name = "Esimerkki"

# KOVAKOODATTUA TESTIJUTTUA YLLÄ, POISTA LOPUKSI

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
    msg['Subject'] = "Tuntikirjauksesi!"

    #tää pitäis toimia loppuversiossa
    #body = get_data()

    body = ''
    body += "Hello World! Näin monta tuntia tulit tehneeksi:\n"
    body += "-"*len(body)
    body += "\n"
    body += "Aloitusaika         Lopetusaika         Projekti       Sää     Selite\n"
    body += f"{start_date}{start_time:<20} {end_date:<10} {end_time:<10} {weather:<10} {assignment}"
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)


#emailin lähetyksen suoritus
send_email()