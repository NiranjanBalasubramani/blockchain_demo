"""
@author: Niranjan Balasubramani
@email: niranjany5070@gmail.com
date: 2018-06-19
"""

from blockchain_app import app
import json
import hashlib
from time import time

class Blockchain(object):
    """
    Blockchain class containing all the entities of a blockchain.
    """

    def __init__(self):
        """
        Constructor of the blockchain class
        :param block_chain: list containing all the blocks in the blockchain
        :param active_transaction: list containing the information about the current active transaction
        """

        self.block_chain = []
        self.active_transaction = []

        # Creating the first block in the blockchain called the 'Genesis block'
        self.create_new_block(proof=100, previous_block_hash=None, current_block_hash='1')


    def create_new_block(self, proof,previous_block_hash=None, current_block_hash=None):
        """
        Creates a new block and adds it to the blockchain
        :param proof: an <int> value called the proof given by the proof_of_work algorithm
        :param previous_block_hash: <str> hash of the previous block in blockchain
        :return: <dict> New block
        """

        print("Proof in CNB: ", proof)
        print("self active transaction: ", self.active_transaction)
        print("previous_block_hash: ",previous_block_hash)

        if previous_block_hash==None:
            previous_block_hash = 'GENESIS block will not have any previous hashes.'

        new_block = {
            'index': len(self.block_chain) + 1,
            'timestamp': time(),
            'transactions': self.active_transaction,
            'proof': proof,
            'previous_block_hash': previous_block_hash,
            'current_block_hash': current_block_hash or self.hash_a_block(self.block_chain[-1])
        }

        print("NEW BLOCK created: ", new_block)

        # Reset the current active transaction
        self.active_transaction = []

        self.block_chain.append(new_block)
        return new_block



    def create_new_transaction(self, sender, recipient, transaction_value):
        """
        Creates a transation to go into the next mined block in the blockchain.
        :param sender: the one who is initiating a transaction
        :param recipient: the one who is receiving the transaction
        :param transaction_value: the value of the transaction taking place; ex: amount
        :return: the index of the block that will hold this value
        """

        self.active_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'transaction_value': transaction_value
        })

        # last_block = self.return_last_block()
        # print("last_blockYOO: ", last_block)
        return self.return_last_block['index'] + 1

    # @staticmethod is a method that knows nothing about the class or instance it was called on. It just gets the argument that were passed
    # https://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python
    @staticmethod
    def hash_a_block(block):
        """
        Creates a SHA-256 hash of a block
        :param: block that has to be hashed
        :return: <str> hash value of the block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        a = hashlib.sha256(block_string).hexdigest()
        print("HASHSIHS: ",a)
        return hashlib.sha256(block_string).hexdigest()

    @property
    def return_last_block(self):
        """
        Returns the last(current) block in the blockchain
        """

        return self.block_chain[-1]

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        last_proof = last_block['proof']
        print("last_proof: ",last_proof)
        last_hash = self.hash_a_block(last_block)
        print("LAST_HASH: ",last_hash)
        proof = 0
        while self.valid_proof(last_proof, proof,last_hash) is False:
            proof += 1

        print("PROOF: ",proof)

        return proof

    # @staticmethod is a method that knows nothing about the class or instance it was called on. It just gets the argument that were passed
    # https://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python
    @staticmethod
    def valid_proof(last_proof, proof,last_hash):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# class Blockchain:
#     def __init__(self):
#         self.current_transactions = []
#         self.chain = []
#         self.nodes = set()
#
#         # Create the genesis block
#         self.new_block(previous_hash='1', proof=100)
#
#     def register_node(self, address):
#         """
#         Add a new node to the list of nodes
#         :param address: Address of node. Eg. 'http://192.168.0.5:5000'
#         """
#
#         parsed_url = urlparse(address)
#         if parsed_url.netloc:
#             self.nodes.add(parsed_url.netloc)
#         elif parsed_url.path:
#             # Accepts an URL without scheme like '192.168.0.5:5000'.
#             self.nodes.add(parsed_url.path)
#         else:
#             raise ValueError('Invalid URL')
#
#     def valid_chain(self, chain):
#         """
#         Determine if a given blockchain is valid
#         :param chain: A blockchain
#         :return: True if valid, False if not
#         """
#
#         last_block = chain[0]
#         current_index = 1
#
#         while current_index < len(chain):
#             block = chain[current_index]
#             print(f'{last_block}')
#             print(f'{block}')
#             print("\n-----------\n")
#             # Check that the hash of the block is correct
#             last_block_hash = self.hash(last_block)
#             if block['previous_hash'] != last_block_hash:
#                 return False
#
#             # Check that the Proof of Work is correct
#             if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
#                 return False
#
#             last_block = block
#             current_index += 1
#
#         return True
#
#     def resolve_conflicts(self):
#         """
#         This is our consensus algorithm, it resolves conflicts
#         by replacing our chain with the longest one in the network.
#         :return: True if our chain was replaced, False if not
#         """
#
#         neighbours = self.nodes
#         new_chain = None
#
#         # We're only looking for chains longer than ours
#         max_length = len(self.chain)
#
#         # Grab and verify the chains from all the nodes in our network
#         for node in neighbours:
#             response = requests.get(f'http://{node}/chain')
#
#             if response.status_code == 200:
#                 length = response.json()['length']
#                 chain = response.json()['chain']
#
#                 # Check if the length is longer and the chain is valid
#                 if length > max_length and self.valid_chain(chain):
#                     max_length = length
#                     new_chain = chain
#
#         # Replace our chain if we discovered a new, valid chain longer than ours
#         if new_chain:
#             self.chain = new_chain
#             return True
#
#         return False
#
#     def new_block(self, proof, previous_hash):
#         """
#         Create a new Block in the Blockchain
#         :param proof: The proof given by the Proof of Work algorithm
#         :param previous_hash: Hash of previous Block
#         :return: New Block
#         """
#
#         block = {
#             'index': len(self.chain) + 1,
#             'timestamp': time(),
#             'transactions': self.current_transactions,
#             'proof': proof,
#             'previous_hash': previous_hash or self.hash(self.chain[-1]),
#         }
#
#         # Reset the current list of transactions
#         self.current_transactions = []
#
#         self.chain.append(block)
#         return block
#
#     def new_transaction(self, sender, recipient, amount):
#         """
#         Creates a new transaction to go into the next mined Block
#         :param sender: Address of the Sender
#         :param recipient: Address of the Recipient
#         :param amount: Amount
#         :return: The index of the Block that will hold this transaction
#         """
#         self.current_transactions.append({
#             'sender': sender,
#             'recipient': recipient,
#             'amount': amount,
#         })
#
#         return self.last_block['index'] + 1
#
#     @property
#     def last_block(self):
#         return self.chain[-1]
#
#     @staticmethod
#     def hash(block):
#         """
#         Creates a SHA-256 hash of a Block
#         :param block: Block
#         """
#
#         # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
#         block_string = json.dumps(block, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()
#
#     def proof_of_work(self, last_block):
#         """
#         Simple Proof of Work Algorithm:
#          - Find a number p' such that hash(pp') contains leading 4 zeroes
#          - Where p is the previous proof, and p' is the new proof
#
#         :param last_block: <dict> last Block
#         :return: <int>
#         """
#
#         last_proof = last_block['proof']
#         last_hash = self.hash(last_block)
#
#         proof = 0
#         while self.valid_proof(last_proof, proof, last_hash) is False:
#             proof += 1
#
#         return proof
#
#     @staticmethod
#     def valid_proof(last_proof, proof, last_hash):
#         """
#         Validates the Proof
#         :param last_proof: <int> Previous Proof
#         :param proof: <int> Current Proof
#         :param last_hash: <str> The hash of the Previous Block
#         :return: <bool> True if correct, False if not.
#         """
#
#         guess = f'{last_proof}{proof}{last_hash}'.encode()
#         guess_hash = hashlib.sha256(guess).hexdigest()
#         return guess_hash[:4] == "0000"
