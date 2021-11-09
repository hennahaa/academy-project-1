 #tämä saattaa joutua vaihtoon, jos nodea ei käytetäkään
 
 #! /bin/bash
sudo su -
umask 077
apt update
apt -y install git-core curl build-essential openssl libssl-dev
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt -y install nodejs
npm install sendgrid
