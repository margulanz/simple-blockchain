from flask import Flask,jsonify

import datetime
import hashlib
import json




class Blockchain:

	def __init__(self):
		self.chain = []
		self.create_block(proof = 1,prev_hash = '0')

	# Creating new block to add to the blockchain
	def create_block(self,proof,prev_hash):
		block = {
			'index':len(self.chain)+1,
			'timestamp':str(datetime.datetime.now()),
			'proof':proof,
			'prev_hash':prev_hash
		}
		self.chain.append(block)
		return block

	# Display previous block
	def print_prev_block(self):
		return self.chain[-1]


	# Miners try to find such number that first 4 digits of the hash are 0's
	def proof_of_work(self,prev_proof):
		new_proof = 1 # Nonce
		check_proof = False
		while check_proof is False:
			hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1
		return new_proof

	def hash(self,block):
		encoded_block = json.dumps(block,sort_keys = True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self,chain):
		prev_block = chain[0]
		block_index = 1
		while block_index < len(chain):
			block = chain[block_index]
			if block['prev_hash'] != self.hash(prev_block):
				return False
			prev_proof = prev_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode())
			if hash_operation[:5] != '00000':
				return False
			prev_block = block
			block_index += 1
		return True

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block',methods = ['GET'])
def mine_block():
	prev_block = blockchain.print_prev_block()
	prev_proof = prev_block['proof']
	proof = blockchain.proof_of_work(prev_proof)
	prev_hash = blockchain.hash(prev_block)
	block = blockchain.create_block(proof,prev_hash)

	response = {
		'message':'Block is mined',
		'index':block['index'],
		'timestamp':block['timestamp'],
		'proof':block['proof'],
		'prev_hash':block['prev_hash']
	}
	return jsonify(response), 200



@app.route('/get_chain',methods = ['GET'])
def display_chain():
	response = {'chain':blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

@app.route('/valid',methods = ['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)
	if valid:
		response = {'message':'Everything is OK'}
	else:
		response = {'message':'blockchain is not valid'}
	return jsonify(reponse),200


app.run(host='127.0.0.1', port=5000)
