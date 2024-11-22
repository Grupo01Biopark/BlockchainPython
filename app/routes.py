import os
import json
from flask import request, jsonify
from datetime import datetime
from app.blockchain import Block
from app.broadcast import broadcast_new_block
from app.mining import mine_new_block

from app import app

@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.json
    agent_id = data.get("agent_id")

    try:
        volume_path = os.path.abspath('/blockchain_data/blockchain.json')

        if not os.path.exists(volume_path):
            return jsonify({"status": "error", "message": f"Arquivo não encontrado: {volume_path}"}), 404

        # Carregar blockchain
        with open(volume_path, "r") as f:
            blockchain_data = json.load(f)

        blockchain = [Block.from_dict(b) for b in blockchain_data]
        last_block = blockchain[-1]

        # Minerar novo bloco
        new_block = mine_new_block(last_block, agent_id)

        blockchain.append(new_block)

        # Salvar blockchain
        with open(volume_path, "w") as f:
            json.dump([b.__dict__ for b in blockchain], f)

        # Propagar novo bloco
        broadcast_new_block(new_block.__dict__)

        return jsonify({"status": "success", "new_block": new_block.__dict__})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
