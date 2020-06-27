# Module 2 - Create a Cryptocurrency


# Importing the libraries
from datetime import datetime
from hashlib import sha256
from json import dumps
from flask import Flask, jsonify, request
from requests import get
from uuid import uuid4
from urllib.parse import urlparse


# Part 1 - Building a blockchain_davidcoin
class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash="0")
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
                "index": len(self.chain) + 1,
                "timestamp": str(datetime.now()),
                "proof": proof,
                "previous_hash": previous_hash,
                "transactions": self.transactions
                }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    @staticmethod
    def hash(block):
        encoded_block = dumps(block, sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transactions(self, sender, receiver, amount):
        self.transactions.append(
            {
                "sender": sender,
                "receiver": receiver,
                "amount": amount
            }
        )
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Part 2 - Mining our blockchain_davidcoin

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace("-", "")

# Creating a blockchain_davidcoin
blockchain = Blockchain()


# Mining a new block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(node_address, "David", 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
                "message": "Congratulation, you just mined a block",
                "index": block["index"],
                "timestamp": block["timestamp"],
                "proof": block["proof"],
                "previous_hash": block["previous_hash"],
                "transactions": block["transactions"]
                }
    return jsonify(response), 200


# Getting the full blockchain_davidcoin
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
                "chain": blockchain.chain,
                "length": len(blockchain.chain)
                }
    return jsonify(response), 200


# Checking if the blockchain_davidcoin is valid
@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid_ = blockchain.is_chain_valid(blockchain.chain)
    if is_valid_:
        response = {"message": "All good. The blockchain_davidcoin is valid."}
    else:
        response = {"message": "BRO, we've a problem. The blockchain_davidcoin isn't valid."}
    return response, 200


# Adding a new transaction to the blockchain
@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all(key in json for key in transaction_keys):
        return "Some elements of the transaction are missing", 400
    index = blockchain.add_transactions(json["sender"], json["receiver"], json["amount"])
    response = {"message": f"This transaction will be added to Block {index}"}
    return jsonify(response), 201


# Part 3 - Decentralizing our blockchain_davidcoin

# Connecting new nodes
@app.route("/connect_node", methods=["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes")
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
            "message": "All the nodes are now connected. The Davidcoin blockchain_davidcoin now contains teh following nodes: ",
            "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


# Replacing the chain by the longest chain if needed
@app.route("/replace_chain", methods=["GET"])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {"message": "The node had different chains so the chain was replaced by the longest one.",
                    "new_chain": blockchain.chain}
    else:
        response = {"message": "All good. The chain is the largest one",
                    "actual_chain": blockchain.chain}
    return response, 200


# Running the app
app.run(host="0.0.0.0", port=5000)
