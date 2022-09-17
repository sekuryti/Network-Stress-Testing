# launch same binary in 100 threads

import os
import sys
import threading


def run():
    os.system(sys.argv[1])
    for i in range(100):
        t = threading.Thread(target=run)
        t.start()


if __name__ == '__main__':
    run()
