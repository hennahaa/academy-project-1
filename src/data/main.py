import psycopg2
from config import config
import json
import urllib.request
import datetime
from dotenv import load_dotenv
import os

# TODO ask information from user and add working time to worktime -table

def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

# check that start date/time is older that end date/time

def check_date(start_date,end_date, start_time, end_time ):
    if start_date > end_date:
        return False
    elif start_time > end_time:
        return False
    else:
        return True

# check that time is valid

def check_validtime(time):
    isValid=False
    while not isValid:
        
        try: # strptime throws an exception if the input doesn't match the pattern
            d = datetime.datetime.strptime(time, '%H:%M')
            isValid=True
        except:
            print("Doh, try again!\n")
            time = input("Give time in format (hh:mm): ")
    return d


# show in screen projects from project -table

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

# Check that project_id what user gave is valid and if not then ask it again

def check_projectid(project_id):
    
    con = None

    row = None

    while row is None:

        try:
            con = psycopg2.connect(**config())
            cur = con.cursor()
            SQL = "SELECT project_id FROM projects WHERE project_id = %s;"
            query_values = project_id
            cur.execute(SQL, query_values)
            row = cur.fetchone()

            if row is None:
                print_projects()
                project_id = input(f"Project id {project_id} was not valid, give another project id: ")
            
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
    return project_id
    
# show users from user -table

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

# Check that user_id what user gave is valid and if not then ask it again

def check_users(user_id):
    
    con = None

    row = None

    while row is None:

        try:
            con = psycopg2.connect(**config())
            cur = con.cursor()
            SQL = "SELECT user_id FROM users WHERE user_id = %s;"
            query_values = user_id
            cur.execute(SQL, query_values)
            row = cur.fetchone()

            if row is None:
                print_users()
                user_id = input(f"User id {user_id} was not valid, give another user id: ")
            
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
    return user_id

# inset one row to worktime -table

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

# find current weather from Helsinki Kaisaniemi (lat=60.18 lon=24.94) and add it to worktime -table temperature -field

def check_weather():
    load_dotenv()
    app_key=os.getenv("APP_KEY")
    search_url = f"https://api.openweathermap.org/data/2.5/weather?lat=60.18&lon=24.94&appid={app_key}"
    weather_file = urllib.request.urlopen(search_url)
    data_info = json.loads(weather_file.read())
    temp_data = ''
    temp_data = data_info['main']['temp']
    celsius_temp = int(temp_data) - 273.15
    return celsius_temp

# user interface where user working time information is asked

def ui():
    print_users()
    user_id = input("Give user id: ")
    user_id = check_users(user_id)
    currenttime = datetime.datetime.now()
    example_time = str(currenttime.hour) + ':' + str(currenttime.minute).zfill(2)
    currentdate = datetime.date.today()
    example_date = currentdate.strftime('%d-%m-%y')
    start_date = input(f"Give start date form is (dd-mm-yy) if you press space default value will be {example_date}: ")
    if start_date == '':
        start_date = example_date
    start_time = input(f"Give start time form is (hh:mm) if you press space default value will be {example_time}: ")
    if start_time == '':
        start_time = example_time
    start_time = check_validtime(start_time)
    end_date = input(f"Give end date form is (dd-mm-yy) if you press space default value will be {example_date}: ")
    if end_date == '':
        end_date = example_date
    end_time = input(f"Give end time form is (hh:mm) if you press space default value will be {example_time}: ")
    if end_time == '':
        end_time = example_time
    end_time = check_validtime(end_time)
    check_date_value = check_date(start_date,end_date, start_time, end_time)
    if check_date_value is True:
        print_projects()
        project_id = input("Give project id: ")
        project_id = check_projectid(project_id)
        comment = input("Give comment (max 255 letters): ")
        temperature = check_weather()
        temp = round(temperature, 2)
        insert_worktime(start_date,start_time,end_date,end_time,project_id,user_id,comment,temp)
    else:
        print(f"Your start values, {start_date} {start_time}, can't be newer than your end values, {end_date} {end_time}.")


if __name__ == '__main__':
    connect()
    print("Welcome to add your work time")
    new_input = 0
    while new_input == 0:
        ui()
        new_input =  int(input("Do you want add another work time (0 = continue): "))