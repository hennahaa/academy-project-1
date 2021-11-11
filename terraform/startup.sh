#! /bin/bash
gsutil cp gs://projekti_ampari/*.py .
gsutil cp gs://projekti_ampari/.env .
sudo apt update
sudo apt -y upgrade
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2
sudo apt -y install python3-pip
sudo pip3 install python-dotenv
sudo pip3 install python-crontab
python cron1.py


#sudo apt-get install postgresql-client
#export dbpass=`gcloud beta secrets versions access 1 --secret="projekti1"`
#psql "sslmode=disable dbname=tuntikirjaus user=postgres hostaddr=34.88.13.245 password=$dbpass"
