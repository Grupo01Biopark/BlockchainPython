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

---

### **Documentação**
- **Projeto**
https://docs.google.com/document/d/18JHgJAH0iNhIE_uvw9wvEL95WOpomrhJcEPP7dOtYOQ/edit?tab=t.0#heading=h.jrbia2my7msq

- **API**
https://www.postman.com/g-carbon/workspace/oillink/collection/28679390-6e87daf8-dba0-4e77-ac73-dc75b8e2b867?action=share&creator=28679390

