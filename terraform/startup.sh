 #! /bin/bash
sudo apt-get update
sudo apt-get install postgresql-client
export dbpass=`gcloud beta secrets versions access 1 --secret="projekti1"`
psql "sslmode=disable dbname=tuntikirjaus user=postgres hostaddr=10.0.1.3 password=$dbpass"