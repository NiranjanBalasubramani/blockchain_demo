from blockchain_app import app
from flask import Flask, jsonify
from blockchain_app.blockchain import Blockchain
from flask import request
from textwrap import dedent
from uuid import uuid4


# Generate a globally unique address for this node
# UUID4() generates a random integer value
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

print("Node_identifier: ", node_identifier)
print("BLOCKCHAIN_INSTANCE: ",blockchain)


# @app.route('/')
# @app.route('/health')
# def index():
#     """
#     Health URL.
#     Returns the json if the flask app is up and running.
#     @return: message string
#     """
#     return jsonify({'message': 'Hello APS Team! Welcome to the Blockchain app.'})
#
# @app.route('/v1/mine', methods=['GET'])
# def mine_block():
#     """
#     Mines a block and verifies proof-of-work
#     :return: a mined block
#     """
#     # We run the proof of work algorithm to get the next proof...
#     last_block = blockchain.return_last_block
#     print("PREVIOUS BLOCK HASH BRO: ", last_block['current_block_hash'])
#     previous_hash = last_block['current_block_hash']
#
#     print("PREVIOUS_HASH: ", previous_hash)
#     # last_proof = last_block['proof']
#     proof = blockchain.proof_of_work(last_block)
#
#     # We must receive a reward for finding the proof.
#     # The sender is "0" to signify that this node has mined a new coin.
#     blockchain.create_new_transaction(
#         sender = "0: Current node that has mined a block has been REWARDED!",
#         recipient = node_identifier,
#         transaction_value = 1
#     )
#
#     # Add the new Block by adding it to the chain
#     current_hash = blockchain.hash_a_block(last_block)
#
#     block = blockchain.create_new_block(proof, previous_hash, current_hash)
#
#     response = {
#         'message': "New Block Added",
#         'index': block['index'],
#         'transactions': block['transactions'],
#         'proof': block['proof'],
#         'previous_block_hash': last_block['current_block_hash'],
#         'current_hash': block['current_block_hash']
#     }
#     return jsonify(response), 200
#
#
# @app.route('/v1/new_transaction', methods=['POST'])
# def new_transaction():
#     """
#     Adds a new transaction to the block
#     :return:
#     """
#     request_data = request.json
#
#     # Check that the required fields are being passed to the API
#     required = ['sender', 'recipient', 'transaction_value']
#     if not all(k in request_data for k in required):
#         return 'Please enter the mandatory `sender`, `recipient` and `transaction_value` values', 400
#
#     sender = request_data.get('sender')
#     recipient = request_data.get('recipient')
#     transaction_value = request_data.get('transaction_value')
#
#
#     # Create a new Transaction
#     index = blockchain.create_new_transaction(sender, recipient, transaction_value)
#
#     response = {'message': 'A new transaction will be added to Block {}'.format(index)}
#     return jsonify(response), 201
#
#
# @app.route('/v1/blockchain', methods=['GET'])
# def chain():
#     """
#     Returns the actual blockchain along with its length
#     :return: <dict> the actual blockchain
#     """
#     response = {
#         'chain': blockchain.block_chain,
#         'length': len(blockchain.block_chain),
#     }
#     return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200