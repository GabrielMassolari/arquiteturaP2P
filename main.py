# -*- coding: utf-8 -*-
import socket
import _thread
import json
import sys
import os

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
        msg_decoded = msg.decode('utf-8')
        string_dict = json.loads(msg_decoded)
        if string_dict["codigo"] == 0:
            pass
        if string_dict["codigo"] == 1:
            pass
        if string_dict["codigo"] == 2:
            pass
        if string_dict["codigo"] == 3:
            pass
        if string_dict["codigo"] == 64:
            pass
        if string_dict["codigo"] == 65:
            pass
        if string_dict["codigo"] == 66:
            pass
        if string_dict["codigo"] == 67:
            pass

def criar_rede_p2p(node):
    node.antecessor = {"id": node.id, "ip": node.ip}
    node.sucessor = {"id": node.id, "ip": node.ip}
    print("Rede P2P inicializada!")
    input("Pressione ENTER para continuar")


def entrar_rede_p2p(node):
    os.system("clear")
    print("-- Entrar Rede P2P --")
    ip = input("Digite o IP do Node: ")


def sair_rede_p2p(node):
    pass


def imprimir_informacoes_node(node):
    os.system("clear")
    print("-- Informações do Nó --")
    print(f"| Id: {node.id}")
    print(f"| Ip: {node.ip}")
    print(f"| Sucessor: {node.sucessor}")
    print(f"| Antecessor: {node.antecessor}")
    print(30 * "-")
    input("Pressione ENTER para continuar")


def interface(node):
    while True:
        os.system("clear")
        print(35 * "-")
        print("| 1 - Criar uma nova rede P2P     |") 
        print("| 2 - Entrar em uma rede P2P      |")
        print("| 3 - Sair da rede P2P            |")
        print("| 4 - Imprimir informacoes do no  |")
        print("| 5 - Sair do programa            |")
        print(35 * "-")
        option = int(input("Digite uma opcao: "))
        
        if option == 1:
            criar_rede_p2p(node)
        elif option == 2:
            entrar_rede_p2p(node)
        elif option == 3:
            sair_rede_p2p(node)
        elif option == 4:
            imprimir_informacoes_node(node)
        elif option == 5:
            sys.exit(0)


def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    node = Node(ip=sys.argv[1])
    _thread.start_new_thread(servidor_p2p, (udp,))
    interface(node)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
    else:
        print("Modo de utilização: python3 main.py <ENDERECO_IP>")
        sys.exit(0)

