# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import psycopg2
import datetime
#from secretmanager import access_secret_version

load_dotenv()

#yhteyden asetusten määritys
def connection():
    return psycopg2.connect(host="192.168.224.3", database="tuntikirjaus", user="postgres", password=os.getenv('KANTA_SALA'))

#Hakee kaikki käyttäjät-listassa olevat henklilöt ja palauttaa siitä listan tupleja
def get_people_info():
    con = None

    try:
        con = connection()
        cur = con.cursor()
        SQL = "SELECT * FROM users;"
        cur.execute(SQL)
        rows = cur.fetchall()

        user_info = []
        for row in rows:
            user_info.append((row[0], f"{row[1]} {row[2]}", row[3]))
        cur.close()

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

#Hakee henkilön työajan summan kyseiseltä päivältä
def work_time(user_id):
    con = None
    worktime = 0

    todays_date= datetime.date.today()
    date = todays_date.strftime('%d-%m-%y')
    
    try:
        con = connection()
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

#Hakee projektit jossa henkilö on kyseisenä päivänä ollut
def project(user_id):
    con = None
    weather = ""
    todays_date= datetime.date.today()
    date = todays_date.strftime('%d-%m-%y')

    try:
        con = connection()
        cur = con.cursor()
        SQL = "SELECT project_name FROM projects INNER JOIN worktime ON projects.project_id = worktime.project_id WHERE worktime.user_id = %s AND worktime.start_date = %s"
        cur.execute(SQL, (user_id,date))
        rows = cur.fetchall()
        project_list = []
        for row in rows:
            project_list.append(row[0])
        cur.close()

        projects = " ".join(project_list)

        return projects

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

#hakee päivälle merkatun sään
def the_weather():
    con = None
    weather = ""
    todays_date= datetime.date.today()
    date = todays_date.strftime('%d-%m-%y')

    try:
        con = connection()
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

#ladataan env
load_dotenv()

#nämä salaisuudet määritellään .env filussa
USERNAME = os.getenv('USERNAME_POSTI')
PASSWORD = os.getenv('PASSWORD_POSTI')
SENDER = os.getenv('SENDER_POSTI')

#muodostetaan viestin runko vastaanottajalle
def get_data(vastaanottaja):
    message = f"Hello, {vastaanottaja[1]}! \n\nYou logged in some work today.\n"
    message += f"You were at work for {work_time(vastaanottaja[0])} hours today. \n"
    message += f"Your hours were logged in project {project(vastaanottaja[0])} \n"
    message += f"\n\nThe weather log today was: {the_weather()}\n"
    message += f"Bye!\n"

    return message
    

def send_email(vastaanottaja):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(USERNAME, PASSWORD)

    fromaddr = SENDER 
    toaddr = vastaanottaja[2] 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your work hours for today"

    #tää pitäis toimia loppuversiossa
    body = get_data(vastaanottaja)
    
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

#emailin lähetyksen suoritus kaikille työntekijöille
if __name__=="__main__":

    info = get_people_info()
    
    for person in info:
        send_email(person)