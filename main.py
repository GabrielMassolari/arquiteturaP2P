# -*- coding: utf-8 -*-
import sys
from p2p import P2P

if __name__ == '__main__':
    if len(sys.argv) == 2:
         servidor = P2P(ip=sys.argv[1])
    else:
        print("Modo de utilização: python3 main.py <ENDERECO_IP>")
        sys.exit(0)

