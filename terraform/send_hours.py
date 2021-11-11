# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import psycopg2
from config import config
import datetime

load_dotenv()

def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def print_projects():
    con = None

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT * FROM users;"
        cur.execute(SQL)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()   
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


def work_time(user_id):
    con = None
    worktime = 0

    todays_date= datetime.date.today()
    date = todays_date.strftime('%d-%m-%y')
    
    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT SUM(end_time - start_time) FROM worktime WHERE user_id = %s and start_date = %s"
        cur.execute(SQL, (user_id, date))
        row = cur.fetchone()
        worktime = row[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    return worktime


def user(user_id):
    con = None
    name = ""

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT user_first_name FROM users WHERE user_id = %s"
        cur.execute(SQL, (user_id,))
        row = cur.fetchone()
        name = row[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    return name

def saa():
    con = None
    weather = ""
    todays_date= datetime.date.today()
    date = todays_date.strftime('%d-%m-%y')

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT weather FROM worktime WHERE start_date = %s"
        cur.execute(SQL, (date,))
        row = cur.fetchone()
        weather = row[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    return weather


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
    msg['Subject'] = "Käyttäjät!"

    #tää pitäis toimia loppuversiossa
    #body = get_data()
    body = work_time()
    
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

def get_data():
    return print_projects

#emailin lähetyksen suoritus
if __name__=="__main__":
    #print_projects()
    #send_email()
    id = 2
    #print(work_time(id))
    #print(user(id))
    #print(saa())
    print(f"{user(id)}'s worktime is {work_time(id)} and weather is {saa()}")

