import shutil
import sys

class LimpaCache:
    @staticmethod
    def limpa_cache():
        cache_dir = "__pycache__"
        shutil.rmtree(cache_dir, ignore_errors=True)
        sys.exit()