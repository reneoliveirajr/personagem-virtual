from interface import Interface
from limpa_cache import LimpaCache
import atexit

if __name__ == '__main__':
    Interface().main()
    atexit.register(LimpaCache.limpa_cache)