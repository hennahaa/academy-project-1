#! /bin/bash
sudo gsutil cp gs://projekti_ampari/*.py .
sudo gsutil cp gs://projekti_ampari/.env .
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
sudo apt-get -y install postgresql-client
sudo pip3 install python-dotenv
sudo pip3 install psycopg2-binary
line="* * * * * python3 /send_hours.py"
(crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -