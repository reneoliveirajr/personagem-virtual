import atexit
from encerra import Encerra
from interface import Interface

if __name__ == '__main__':
    Interface().main()
    atexit.register(Encerra.encerra)