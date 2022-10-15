from node import Node
import socket
import multiprocessing as mp
import json
import os
import sys


class ServidorP2P:
    def __init__(self, ip=None):
        self.node = Node(ip=sys.argv[1])
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__t1 = mp.Process(target=self.controle)
        self.__t1.start()
        self.interface()


    def servidor(self):
        print(f"Starting P2P Server on port {self.node.porta}")
        orig = ("", self.node.porta)
        self.udp.bind(orig)
        while True:
            msg, cliente = self.udp.recvfrom(1024)
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


    def criar_rede_p2p(self):
        self.node.antecessor = {"id": self.node.id, "ip": self.node.ip}
        self.node.sucessor = {"id": self.node.id, "ip": self.node.ip}
        self.node._inicializado = True
        print("Rede P2P inicializada!")
        input("Pressione ENTER para continuar")


    def entrar_rede_p2p(self):
        os.system("clear")
        print("-- Entrar Rede P2P --")
        ip = input("Digite o IP do Node: ")


    def sair_rede_p2p(self):
        pass


    def imprimir_informacoes_node(self):
        os.system("clear")
        print("-- Informações do Nó --")
        print(f"| Id: {self.node.id}")
        print(f"| Ip: {self.node.ip}")
        print(f"| Sucessor: {self.node.sucessor}")
        print(f"| Antecessor: {self.node.antecessor}")
        print(30 * "-")
        input("Pressione ENTER para continuar")


    def interface(self):
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
                self.criar_rede_p2p()
            elif option == 2:
                self.entrar_rede_p2p()
            elif option == 3:
                self.sair_rede_p2p()
            elif option == 4:
                self.imprimir_informacoes_node()
            elif option == 5:
                sys.exit(0)
