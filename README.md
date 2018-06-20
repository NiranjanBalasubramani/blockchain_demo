Synopsis
A Python app with all the necessary functionalities of blockchain technology.

Python version used - 3.6.5

Installation
To install the code follow the steps outlined here -

Step 1 - Ensure all the dependencies are present
sudo apt-get install -y ipython3 python3-dev build-essential libssl-dev libffi-dev git python-virtualenv

Step 3 - Clone repo from git

git clone ssh://git@stash.akamai.com:7999/aps/traceheaders-cracker.git traceheaders
cd /var/www/traceheaders/



Step 4 - Create a python virtual environment and install python packages
cd /var/www/traceheaders/
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

Step 5 - Run Flask on your terminal
python run_server.py
flask run

Configuration
All the app specific basic configuration will be under config.py file

Contributors
Niranjan - niranjany5070@gmail.com
