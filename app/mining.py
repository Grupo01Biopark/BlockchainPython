from app.blockchain import Block
from datetime import datetime


def mine_new_block(last_block, agent_id):
    new_data = f"Bloco minerado por agente {agent_id} em {datetime.utcnow().isoformat()}"
    new_block = Block(
        index=last_block.index + 1,
        timestamp=datetime.utcnow().isoformat(),
        data=new_data,
        previous_hash=last_block.hash,
        sensor_type=last_block.sensor_type,
        agent_id=agent_id,
    )

    difficulty = 4
    new_block.mine_block(difficulty)
    return new_block
