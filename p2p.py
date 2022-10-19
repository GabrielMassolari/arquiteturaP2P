from node import Node
import socket
import multiprocessing as mp
import json
import os
import sys
import time


class P2P:
    def __init__(self, ip=None):
        self.node = Node(ip=sys.argv[1])
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__t1 = mp.Process(target=self.controle)
        self.__t1.start()
        self.interface()


    def lookup_request(self, ip):
        msg = {
            "codigo": 2,
            "identificador": self.node.id,
            "ip_origem_busca": self.node.ip,
            "id_busca": self.node.id,
        }
        msg_json = json.dumps(msg)
        dest = (ip, self.node.porta)
        self.udp.sendto(msg_json.encode('utf-8'), dest)


    def reply_lookup_request(self, msg, ip):
        dest = (ip, self.node.porta)
        self.udp.sendto(msg.encode('utf-8'), dest)
        

    def send_lookup_confirmation(self, string_dict):
        msg = {
            "codigo": 66,
            "id_busca": string_dict["id_busca"],
            "id_origem": string_dict["identificador"],
            "ip_origem": string_dict["ip_origem_busca"],
            "id_sucessor": self.node.id,
            "ip_sucessor": self.node.ip
        }

        msg_json = json.dumps(msg)
        dest = (string_dict["ip"], self.node.porta)
        self.udp.sendto(msg_json.encode('utf-8'), dest)


    def response_lookup_request(self, string_dict):
        #verificar se ha um unico Node na rede
        if self.node.antecessor == self.node.sucessor:
            self.send_lookup_confirmation(string_dict)
        #Verifica se e o primeiro da fila
        elif self.node.antecessor["id"] > self.node.id:
            if self.node.antecessor["id"] < string_dict["identificador"]:
                self.send_lookup_confirmation(string_dict)
        else:
            #Envia o lookup para o proximo Node
            if string_dict["identificador"] > self.node.id:
                self.reply_lookup_request(string_dict, self.node.sucessor["ip"])
            else:
                self.send_lookup_confirmation(string_dict)


    def join_request(self, string_dict):
        msg = {
            "codigo": 0,
            "id": string_dict["id_origem"]
        }
        msg_json = json.dumps(msg)
        dest = (string_dict["ip_sucessor"], self.node.porta)
        self.udp.sendto(msg_json.encode('utf-8'), dest)


    def response_lookup_confirmation(self, string_dict):
        self.join_request(string_dict)


    def response_join_request(self, cliente):
        #q
        msg = {
            "codigo": 64,
            "id_sucessor": self.node.id,
            "ip_sucessor": self.node.ip,
            "id_antecessor": self.node.antecessor["id"],
            "ip_antecessor": self.node.antecessor["ip"]
        } 
        msg_json = json.dumps(msg)
        self.udp.sendto(msg_json.encode('utf-8'), cliente)


    def update_sucessor(self, id, ip):
        #q
        msg = {
            "codigo": 3,
            "identificador": self.node.id,
            "id_novo_antecessor": id,
            "ip_novo_antecessor": ip
        }
        dest = (self.node.sucessor["ip"], self.node.porta)
        msg_json = json.dumps(msg)
        self.udp.sendto(msg_json.encode('utf-8'), dest)
        

    def update_antecessor(self, id, ip):
        msg = {
            "codigo": 3,
            "identificador": self.node.id,
            "id_novo_sucessor": id,
            "ip_novo_sucessor": ip
        }
        dest = (self.node.antecessor["ip"], self.node.porta)
        msg_json = json.dumps(msg)
        self.udp.sendto(msg_json.encode('utf-8'), dest)


    def update_response(self, string_dict, cliente):
        if "id_novo_antecessor" in string_dict:
            self.node.antecessor["id"] = string_dict["id_novo_antecessor"]
            self.node.antecessor["ip"] = string_dict["ip_novo_antecessor"]
        else:
            self.node.sucessor["id"] = string_dict["id_novo_sucessor"]
            self.node.sucessor["ip"] = string_dict["ip_novo_sucessor"]
        #q
        msg = {
            "codigo": 67,
            "id_origem_mensagem": string_dict["identificador"]
        }
        msg_json = json.dumps(msg)
        self.udp.sendto(msg_json.encode('utf-8'), cliente)


    def update_confirmation(self):
        #To Debug
        print("Update confirmado")


    def join_response(self, string_dict):
        self.node.sucessor = {"id": string_dict["id_sucessor"], "ip": string_dict["ip_sucessor"]}
        self.node.antecessor = {"id": string_dict["id_sucessor"], "ip": string_dict["ip_sucessor"]}
        self.update_antecessor(self.node.id, self.node.ip)
        self.update_sucessor(self.node.id, self.node.ip)

    
    def leave_request(self):
        if self.node.antecessor["id"] == self.node.sucessor["id"]:
            self.node.sucessor = {"id": None, "ip": None}
            self.node.antecessor = {"id": None, "ip": None}
        else:
            msg = {
                "codigo": 1,
                "identificador": self.node.id,
                "id_sucessor": self.node.sucessor["id"],
                "ip_sucessor": self.node.sucessor["ip"],
                "id_antecessor": self.node.antecessor["id"],
                "ip_antecessor": self.node.antecessor["ip"]
            }
            destAnt = (self.node.antecessor["ip"], self.node.porta)
            destSuc = (self.node.sucessor["ip"], self.node.porta)
            msg_json = json.dumps(msg)
            self.udp.sendto(msg_json.encode('utf-8'), destAnt)
            self.udp.sendto(msg_json.encode('utf-8'), destSuc)


    def leave_response(self, string_dict, cliente):
        if string_dict["identificador"] == self.node.antecessor["id"]:
            self.node.antecessor["id"] = string_dict["id_antecessor"]
            self.node.antecessor["ip"] = string_dict["ip_antecessor"]
        else:
            self.node.sucessor["id"] = string_dict["id_sucessor"]
            self.node_sucessor["ip"] = string_dict["ip_sucessor"]
        
        msg = {
            "codigo": 65,
            "identificador": string_dict["identificador"]
        }
        msg_json = json.dumps(msg)
        self.udp.sendto(msg_json.encode('utf-8'), cliente)

    
    def leave_confirmation(self):
        #To Debug
        print("Alteracao de saida confirmada")


    def servidor(self):
        print(f"Starting P2P Server on port {self.node.porta}")
        orig = ("", self.node.porta)
        self.udp.bind(orig)
        while True:
            msg, cliente = self.udp.recvfrom(1024)
            msg_decoded = msg.decode('utf-8')
            string_dict = json.loads(msg_decoded)
            if string_dict["codigo"] == 0:
                self.response_join_request(cliente)
            elif string_dict["codigo"] == 1:
                self.leave_response(string_dict, cliente)
            elif string_dict["codigo"] == 2:
                self.response_lookup_request(string_dict)
            elif string_dict["codigo"] == 3:
                self.update_response(string_dict, cliente)
            elif string_dict["codigo"] == 64:
                self.join_response(string_dict)
            elif string_dict["codigo"] == 65:
                self.leave_confirmation()
            elif string_dict["codigo"] == 66:
                self.response_lookup_confirmation(string_dict)
            elif string_dict["codigo"] == 67:
                self.update_confirmation()


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
        self.lookup_request(ip)
        time.sleep(5)
        

    def sair_rede_p2p(self):
        self.leave_request()
        time.sleep(5)


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
