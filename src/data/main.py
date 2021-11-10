import psycopg2
from config import config
import json
import urllib.request
import datetime

def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def check_date(start_date,end_date):
    if start_date > end_date:
        return False
    else:
        return True

def print_projects():
    con = None

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT * FROM projects;"
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
    

def print_users():
    con = None

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "SELECT * FROM users;"
        cur.execute(SQL)
        row = cur.fetchone()

        while row is not None:
            user_id = row[0]
            user_first_name = row[1]
            user_last_name = row[2]
            print(f"{user_id}, {user_first_name} {user_last_name}")
            row = cur.fetchone()
        
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    pass

def insert_worktime(start_date,start_time,end_date,end_time,project_id,user_id,comment,temperature):
    con = None

    try:
        con = psycopg2.connect(**config())
        cur = con.cursor()
        SQL = "INSERT INTO worktime (start_date, start_time, end_date, end_time, assignment, weather, project_id, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        insert_values = (start_date,start_time,end_date,end_time,comment,temperature,project_id,user_id)
        cur.execute(SQL, insert_values)
        con.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def check_weather():
    weather_file = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?lat=60.18&lon=24.94&appid=e8b0924d5a0ce89fd664d80238a253c3")
    data_info = json.loads(weather_file.read())
    temp_data = ''
    temp_data = data_info['main']['temp']
    celsius_temp = int(temp_data) - 273.15
    print(f"Its {celsius_temp:.2f} celcius")
    return celsius_temp

def ui():
    print_users()
    user_id = input("Give user id: ")
    currenttime = datetime.datetime.now()
    example_time = str(currenttime.hour) + ':' + str(currenttime.minute)
    currentdate = datetime.date.today()
    example_date = currentdate.strftime('%d-%m-%y')
    start_date = input(f"Give start date ({example_date}): ")
    start_time = input(f"Give start time ({example_time}): ")
    end_date = input("Give end date (dd-mm-yy): ")
    end_time = input("Give end time (hh:mm): ")
    check_date_value = check_date(start_date,end_date)
    if check_date_value is True:
        print_projects()
        project_id = input("Give project id: ")
        comment = input("Give comment (max 255 letters): ")
        temperature = check_weather()
        temp = round(temperature, 2)
        insert_worktime(start_date,start_time,end_date,end_time,project_id,user_id,comment,temp)
    else:
        print(f"Your start date, {start_date}, can't be newer than your end_date, {end_date}.")


if __name__ == '__main__':
    connect()
    check_weather()
    #print("Welcome! Add your work time")
    #new_input = 0
    #while new_input == 0:
    #    ui()
    #    new_input =  int(input("Do you want add another work time (0 = continue): "))