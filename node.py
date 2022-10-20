from random import randint

class Node:
    def __init__(self, ip):
        self.ip = ip
        #self.id = hash(f"{ip}+gabrielg")
        self.id = randint(1, 1000)
        self.porta = 12345
        self.sucessor = None
        self.antecessor = None
