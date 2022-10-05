import socket
import _thread
import json

PORT = 12345


class Node:
    def __init__(self, ip):
        self.ip = ip
        self.id = hash(f"{ip}+gabrielg")
        self.porta = None
        self.sucessor = None
        self.antecessor = None


def servidor_p2p(udp):
    print(f"Starting P2P Server on port {PORT}")
    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, cliente = udp.recvfrom(1024)


def interface(node):
    while True:
        pass


def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    node = Node()
    _thread.start_new_thread(servidor_p2p, (udp,))
    _thread.start_new_thread(interface, (node,))


if __name__ == '__main__':
    main()