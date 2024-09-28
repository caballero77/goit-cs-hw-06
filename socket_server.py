import json
import logging
import socket
import os
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

host = 'localhost'
port = int(os.getenv("SOCKET_PORT", 5000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

db_name = os.getenv("DB_NAME", "chat")
db_collection = os.getenv("DB_COLLECTION", "messages")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 27017))
db_user = os.getenv("DB_USER", "user")
db_password = os.getenv("DB_PASSWORD", "password")


def save_message(data_dict):
    with MongoClient(host=db_host, port=db_port, username=db_user, password=db_password) as client:
        db = client[db_name]
        collection = db[db_collection]
        collection.insert_one(data_dict)
        logging.info(f"Message saved: {data_dict}")
        logging.info(collection.count_documents({}))
        client.close()


def run_socket_server():
    while True:
        client, address = server.accept()
        message = client.recv(4096).decode('utf-8')
        logging.info(f"Received message: {message}")
        data_dict = json.loads(message)
        save_message(data_dict)
