from flask import Flask
from os import environ

app = Flask(__name__)

app.config.from_object("config.Config")

from blockchain_app import views
