import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len( self.chain ) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash( self.chain[ -1 ] )
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Append the block to the chain

        self.chain.append( block )
        # Return the new block
        return block

    def hash(self, block):
        string_object = json.dumps( block, sort_keys=True )

        # TODO: Create the block_string
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256( block_string )

        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self):
        block_string = json.dumps( self.last_block, sort_keys=True )

        proof = 0
        print('enter')

        while self.valid_proof( block_string, proof ) is False:
            proof += 1

        print('found', proof)
        return proof

    @staticmethod
    def valid_proof(block_string, proof):
        guess = f"{block_string}{proof}".encode()
        hash_guess = hashlib.sha256( guess ).hexdigest()
        # return True or False
        return hash_guess[:3] == "000"

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify( blockchain.last_block )

@app.route('/mine', methods=['GET'])
def mine():
    data = request.get_json()
    print( 'HERE------>', data )
    if data.id and data.proof:        
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash( blockchain.last_block ) 
        new_block = blockchain.new_block( proof, previous_hash )

        response = {
            # TODO: Send a JSON response with the new block
            'index': new_block['index'],
            'transactions': new_block['transactions'],
            'proof': new_block['proof'],
            'previous_hash': new_block['previous_hash']
        }

        return jsonify(response), 200
    
    else: 
        response = {
            message: "Proof Failed"
        }

        return jsonify( response ), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len( blockchain.chain )
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
