import logging
import re
import socket
import sys
import json


class Server:
    def __init__(self):
        self.__ip = None
        self.__port = None
        self.__addr = None
        # based on TCP/IP system
        self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_sock = None

    def __init(self, backlog):
        server_addr = (self.__ip, self.__port)
        self.__server_sock.bind(server_addr)
        self.__server_sock.listen(backlog)

    def init(self, ip, port):
        # IPv6 system doesn't support
        ip_check_string = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        is_valid_ip = re.match(ip_check_string, ip) is not None

        if type(ip) == str and is_valid_ip:
            self.__ip = ip
        if type(port) == int:
            self.__port = port

        if self.__ip is None or self.__port is None:
            raise AttributeError

        backlog = 2  # only two connection are valid
        self.__init(backlog)

    def accept(self):
        self.__client_sock, self.__addr = \
            self.__server_sock.accept()
        logging.info('connected in ==> {}'.format(self.__addr))

    def receive(self, recv_size):
        recv_data = (self.__client_sock.recv(recv_size)).decode('utf-8')
        logging.info('receive data ==> {}'.format(recv_data))
        return recv_data

    def send(self, data):
        if type(data) == str:
            self.__client_sock.send(data.encode('utf-8'))

    def __del__(self):
        if self.__server_sock is not None:
            self.__server_sock.close()
        if self.__client_sock is not None:
            self.__client_sock.close()


class Client:
    def __init__(self):
        self.__ip = None
        self.__port = None
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init(self):
        con_addr = (self.__ip, self.__port)
        try:
            self.__client_sock.connect(con_addr)
        except ConnectionError:
            logging.error("cannot connect ==> {}".format(con_addr))
            sys.exit()

    def init(self, ip, port):
        # IPv6 system doesn't support
        ip_check_string = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        is_valid_ip = re.match(ip_check_string, ip) is not None

        if type(ip) == str and is_valid_ip:
            self.__ip = ip
        if type(port) == int:
            self.__port = port

        if self.__ip is None or self.__port is None:
            raise AttributeError

        self.__init()

    def receive(self, recv_size):
        recv_data = self.__client_sock.recv(recv_size).decode('utf-8')
        logging.info('receive data ==> {}'.format(recv_data))
        return recv_data

    def send(self, data):
        if type(data) == str:
            self.__client_sock.send(data.encode('utf-8'))

    def __del__(self):
        if self.__client_sock is not None:
            self.__client_sock.close()

class Communication:
    @staticmethod
    def receive_data(_sock):
        length = _sock.receive(256)
        if length.isdecimal():
            length = int(length)
        else:
            raise ConnectionError
        _sock.send("OK")
        recv_data = json.loads(_sock.receive(length))
        return recv_data

    @staticmethod
    def send_data(_sock, _buffer):
        data = json.dumps(_buffer)
        _sock.send(str(len(data.encode())))
        if _sock.receive(256) == 'OK':
            _sock.send(data)
