from blockchain_app import app
from flask import jsonify
from blockchain_app import blockchain

@app.route('/')
@app.route('/health')
def index():
    """
    Health URL.
    Returns the json if the flask app is up and running.
    @return: message string
    """
    return jsonify({'message': 'Hello APS Team! Welcome to the Blockchain app.'})