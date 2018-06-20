Synopsis
A Python app with all the necessary functionalities of blockchain technology.

Python version used - 3.6.5

Installation
To install the code follow the steps outlined here -

Step 1 - Ensure all the dependencies are present
    sudo apt-get install -y ipython3 python3-dev build-essential libssl-dev libffi-dev git python-virtualenv

Step 2 - Get into your home directory
    cd ~

Step 3 - Clone repo from git
    git clone https://github.com/NiranjanBalasubramani/blockchain_demo.git
    cd ~/blockchain_demo

Step 4 - Create a python virtual environment and install python packages
    cd ~/blockchain_demo/
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt

Step 5 - Run flask on your terminal
    python run_server.py # This will run the app in blocking mode.

Step 6 (OPTIONAL) - If you want to run the app in the background, you can use supervisor package to do so...
    sudo apt-get install supervisor
    cd /etc/supervisor/conf.d/blockchain.conf
        #name of the process
        [program:blockchain]

        #command to run
        command=/<your_home_directory>/blockchain_demo/env/bin/gunicorn blockchain_app:app -b localhost:5030 --workers=1
        #complete path to your application directory
        directory = /<your_home_directory>/blockchain_demo

        #User to run the process with
        user = <your user>

        #Start process at system boot
        autostart=true

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start blockchain

Configuration
All the app specific basic configuration will be under config.py file

Contributors
Niranjan - niranjany5070@gmail.com
