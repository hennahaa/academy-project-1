#! /bin/bash
sudo apt update && sudo apt upgrade 
sudo apt install python3-pip
sudo pip3 install python-dotenv
sudo pip3 install crontab
gsutil cp gs://projekti_ampari/testi.txt . #kesken