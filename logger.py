import time


class PerformanceLogger:
    def __init__(self):
        self._start = 0.0

    def start(self, name):
        print(f"======= {name} Start =======")
        self._start = time.time()

    def log(self):
        elapsed = time.time() - self._start
        print('{:3.3} seconds elapsed'.format(elapsed))
