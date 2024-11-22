import json
import os
import socket
from app.blockchain import Block


BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", BROADCAST_PORT))


def handle_broadcast_message(message):
    """Processa mensagens broadcast com base no tipo."""
    message_type = message.get("type")

    if message_type == "new_block":
        block_data = message.get("block")
        handle_new_block(block_data)
    elif message_type == "sync_request":
        respond_to_sync_request()
    elif message_type == "sync_response":
        handle_sync_response(message)
    else:
        print(f"Mensagem desconhecida recebida: {message_type}")


def broadcast_new_block(block_data):
    try:
        message = {"type": "new_block", "block": block_data}
        sock.sendto(json.dumps(message).encode(), (BROADCAST_IP, BROADCAST_PORT))
        print(f"Broadcast de novo bloco enviado: {message}")
    except Exception as e:
        print(f"Erro ao enviar broadcast: {e}")


def broadcast_sync_request():
    message = {"type": "sync_request"}
    sock.sendto(json.dumps(message).encode(), (BROADCAST_IP, BROADCAST_PORT))
    print("Broadcast de sincronização enviado.")

def listen_for_broadcast():
    """Escuta mensagens broadcast e processa."""
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Recebe mensagens
            message = json.loads(data.decode())

            # Validar e processar mensagens
            if validate_proof_of_work(message):  # Adicione a função de validação no lugar correto
                handle_broadcast_message(message)
            else:
                print(f"Mensagem inválida recebida de {addr}. Falhou na validação de PoW.")
        except Exception as e:
            print(f"Erro ao processar mensagem de broadcast: {e}")


def validate_proof_of_work(message):
    """Valida o Proof of Work de um bloco."""
    from app.blockchain import Block  # Importação local para evitar referência circular
    block_data = message.get("block")
    if not block_data:
        return False

    block = Block.from_dict(block_data)
    return block.hash.startswith("0000")  # Critério para validação


def respond_to_sync_request():
    """Responde a solicitações de sincronização enviando o blockchain local."""
    volume_path = os.path.abspath('/blockchain_data/blockchain.json')

    if os.path.exists(volume_path):
        # Ler o blockchain local
        with open(volume_path, "r") as f:
            blockchain_data = json.load(f)

        # Criar mensagem de resposta
        message = {"type": "sync_response", "blockchain": blockchain_data}

        # Enviar resposta via broadcast
        sock.sendto(json.dumps(message).encode(), (BROADCAST_IP, BROADCAST_PORT))
        print("Resposta de sincronização enviada.")
    else:
        print(f"Arquivo {volume_path} não encontrado. Não foi possível responder à solicitação de sincronização.")

def handle_sync_response(message):
    blockchain_data = message.get("blockchain")
    volume_path = os.path.abspath('/blockchain_data/blockchain.json')

    if blockchain_data:
        if os.path.exists(volume_path):
            with open(volume_path, "r") as f:
                local_blockchain_data = json.load(f)

            if len(blockchain_data) > len(local_blockchain_data):
                with open(volume_path, "w") as f:
                    json.dump(blockchain_data, f)
                print("Blockchain atualizado com sucesso.")
            else:
                print("Blockchain local já está atualizado.")


def handle_new_block(block_data):
    volume_path = os.path.abspath('/blockchain_data/blockchain.json')

    if os.path.exists(volume_path):
        with open(volume_path, "r") as f:
            blockchain_data = json.load(f)

        blockchain = [Block.from_dict(b) for b in blockchain_data]
        new_block = Block.from_dict(block_data)

        if new_block.previous_hash == blockchain[-1].hash:
            blockchain.append(new_block)

            with open(volume_path, "w") as f:
                json.dump([b.__dict__ for b in blockchain], f)
            print(f"Novo bloco adicionado.")
