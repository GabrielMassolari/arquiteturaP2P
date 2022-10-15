class Node:
    def __init__(self, ip):
        self.ip = ip
        self.id = hash(f"{ip}+gabrielg")
        self.porta = 12345
        self.sucessor = None
        self.antecessor = None
