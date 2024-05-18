import socket
from _thread import start_new_thread
import select
import sys
from thread import *
from typing import Union
from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel


def get_logger(name=__file__, file='log.txt', encoding='utf-8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []


def clientthread(conn, addr):
    logger.info("Welcome to this chatroom!")
    conn.send("Welcome to this chatroom!")

    while True:
        try:
            message = conn.recv(2048)
            if message:
                message_to_send = "<" + addr[0] + "> " + message
                print(message_to_send)
                logger.info(message_to_send)
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            logger.info('Error')
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                # if the link is broken, we remove the client
                logger.debug('Line is broken')
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    logger.info(addr[0] + " connected")
    start_new_thread(clientthread, (conn, addr))


conn.close()
server.close()

