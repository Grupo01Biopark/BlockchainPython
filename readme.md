# **Blockchain Agent Management API**

## **Descrição**
Este projeto fornece uma API para gerenciar agentes baseados em contêineres Docker que operam blockchains descentralizados. Cada agente representa um nó na rede blockchain e possui seu próprio blockchain local. O sistema permite criar agentes, listar agentes em execução e inicializar blockchains com blocos gênesis.

---

## **Instalação**

### **Requisitos**
- **Python 3.8+**
- **Docker** e **Docker Compose**
- Rede Docker chamada `blockchain` criada previamente:
  ```bash
  docker network create blockchain
- Dependencias instaladas
  ```bash
  pip install docker
  pip install flask
  

- Configure a imagem do agente Docker: Crie ou certifique-se de que a imagem Docker chamada agent está configurada para os agentes:
  ```bash
  docker build -t agent .

- Execute o servidor
  ```bash
  python AgentController.py
