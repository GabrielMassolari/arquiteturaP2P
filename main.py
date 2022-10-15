# -*- coding: utf-8 -*-
import sys
from node import Node
from servidorp2p import ServidorP2P

if __name__ == '__main__':
    if len(sys.argv) == 2:
         servidor = ServidorP2P(ip=sys.argv[1])
    else:
        print("Modo de utilização: python3 main.py <ENDERECO_IP>")
        sys.exit(0)

