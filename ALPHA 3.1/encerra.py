import shutil
import sys


class Encerra:
    @staticmethod
    def encerra():
        cache_dir = "__pycache__"
        shutil.rmtree(cache_dir, ignore_errors=True)
        sys.exit()