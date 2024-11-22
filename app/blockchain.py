import hashlib
import uuid
from datetime import datetime
import random


class Block:
    def __init__(self, index, timestamp, data, previous_hash='', sensor_type='', agent_id='', nonce=None, latitude=None, longitude=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.sensor_type = sensor_type
        self.agent_id = agent_id
        self.nonce = nonce or str(uuid.uuid4())
        self.latitude = latitude or self.generate_random_latitude()
        self.longitude = longitude or self.generate_random_longitude()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.sensor_type}{self.agent_id}{self.nonce}{self.latitude}{self.longitude}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce = str(uuid.uuid4())
            self.hash = self.calculate_hash()

    @staticmethod
    def generate_random_latitude():
        """Gera uma latitude aleatória no intervalo de -90 a 90 graus."""
        return round(random.uniform(-90, 90), 6)

    @staticmethod
    def generate_random_longitude():
        """Gera uma longitude aleatória no intervalo de -180 a 180 graus."""
        return round(random.uniform(-180, 180), 6)

    @staticmethod
    def from_dict(block_dict):
        return Block(
            index=block_dict['index'],
            timestamp=block_dict['timestamp'],
            data=block_dict['data'],
            previous_hash=block_dict['previous_hash'],
            sensor_type=block_dict['sensor_type'],
            agent_id=block_dict['agent_id'],
            nonce=block_dict['nonce'],
            latitude=block_dict.get('latitude'),
            longitude=block_dict.get('longitude')
        )


def create_genesis_block(sensor_type, agent_id):
    return Block(0, datetime.utcnow().isoformat(), "Bloco de gênesis - Inicialização da cadeia", "0", sensor_type, agent_id)
