import hashlib
import json
import os
from datetime import datetime
import docker
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)
client = docker.from_env()


class Block:
    def __init__(self, index, timestamp, data, previous_hash='', sensor_type='', agent_id='', nonce=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.sensor_type = sensor_type
        self.agent_id = agent_id
        self.nonce = nonce or str(uuid.uuid4())
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.sensor_type}{self.agent_id}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def from_dict(data_dict):
        data_dict.pop('hash', None)
        return Block(**data_dict)


def create_genesis_block(sensor_type, agent_id):
    return Block(0, datetime.utcnow().isoformat(), "Bloco de gênesis - Inicialização da cadeia", "0", sensor_type, agent_id)


def create_agent(sensor_type, port):
    try:
        container_name = f"agent_{sensor_type}_{len(client.containers.list()) + 1}"
        agent_id = container_name
        genesis_block = create_genesis_block(sensor_type, agent_id)

        # Criar diretório para o agente
        volume_path = os.path.abspath(f"./blockchain_data/{container_name}")
        os.makedirs(volume_path, exist_ok=True)
        blockchain_file_path = os.path.join(volume_path, 'blockchain.json')

        # Criar blockchain inicial
        if not os.path.exists(blockchain_file_path):
            with open(blockchain_file_path, "w") as f:
                json.dump([genesis_block.__dict__], f)

        # Criar o contêiner
        container = client.containers.run(
            "agent",
            name=container_name,
            detach=True,
            ports={f"{5001}/tcp": port},
            volumes={volume_path: {'bind': '/blockchain_data', 'mode': 'rw'}},
            network="blockchain"
        )

        return {
            "status": "success",
            "container_id": container.id,
            "sensor_type": sensor_type,
            "port": port,
            "genesis_block": genesis_block.__dict__
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route('/create_agent', methods=['POST'])
def create_agent_api():
    data = request.json
    sensor_type = data.get("sensor_type")
    port = data.get("port")

    if not sensor_type or not port:
        return jsonify({"status": "error", "message": "Os campos 'sensor_type' e 'port' são obrigatórios"}), 400

    result = create_agent(sensor_type, port)
    return jsonify(result)

@app.route('/list_agents', methods=['GET'])
def list_agents():
    try:
        containers = client.containers.list(filters={"name": "agent_"})
        agents = []

        for container in containers:
            container_info = {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "ports": container.attrs['NetworkSettings']['Ports'],
            }
            agents.append(container_info)

        return jsonify({"status": "success", "agents": agents})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
