#connect to Cloud SQL instance:

gcloud sql connect week5-group2 --user=postgres

#Create database:
CREATE DATABASE tuntikirjaus;

#connect to database:
\connect tuntikirjaus;

#create user table and insert data:

CREATE TABLE users (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_first_name VARCHAR(255) NOT NULL,
    user_last_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255)
);
#make email unique
ALTER TABLE users ADD UNIQUE (user_email);

INSERT INTO users (user_first_name, user_last_name, user_email) values ('Henna', 'Haapala', 'henna.haapala@projekti1.com');
INSERT INTO users (user_first_name, user_last_name, user_email) values ('Kirsi', 'Holmberg', 'kirsi.holmberga@projekti1.com');
INSERT INTO users (user_first_name, user_last_name, user_email) values ('JP', 'HeinO', 'jp.heino@projekti1.com');

#create projects table
CREATE TABLE projects (
    project_id int NOT NULL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL
);

INSERT INTO projects (project_id, project_name) values (1, 'Frontend');
INSERT INTO projects (project_id, project_name) values (2, 'Backend');
INSERT INTO projects (project_id, project_name) values (3, 'Merging');


#create worktime table which will be user to collect daily worktime data
CREATE TABLE worktime (
    start_date DATE NOT NULL, 
    start_time DATE NOT NULL, 
    end_date DATE NOT NULL, 
    end_time DATE NOT NULL, 
    assignment VARCHAR(255) NOT NULL,
    weather VARCHAR(255), 
    project_id INTEGER REFERENCES projects (project_id) NOT NULL, 
    user_id INTEGER REFERENCES users (user_id) NOT NULL);

#show data:
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM worktime;

#change datetime datatype into date and time:
ALTER TABLE worktime
ALTER COLUMN start_time TYPE TIME
USING start_time::time;

ALTER TABLE worktime
ALTER COLUMN end_time TYPE time
USING end_time::time without time zone;

#could not change data type, lets drop the table and create new:

DROP TABLE worktime;

#create new:

CREATE TABLE worktime (
    start_date DATE NOT NULL, 
    start_time TIME NOT NULL, 
    end_date DATE NOT NULL, 
    end_time TIME NOT NULL, 
    assignment VARCHAR(255) NOT NULL,
    weather VARCHAR(255), 
    project_id INTEGER REFERENCES projects (project_id) NOT NULL, 
    user_id INTEGER REFERENCES users (user_id) NOT NULL);