# fuzz ntp server with ntpd and try to crash it

import os
import sys
import time
import random
import string
import subprocess


def main():
    if len(sys.argv) != 2:
        print("Usage: fuzz_ntp.py <path to ntpd>")
        sys.exit(1)

    ntpd_path = sys.argv[1]
    if not os.path.exists(ntpd_path):
        print("ntpd binary not found")
        sys.exit(1)

    while True:
        # generate random string
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))

        # create config file
        config_file = open("fuzz.conf", "w")
        config_file.write("server") 
        config_file.write("fuzz.log")
        config_file.close()


        # run ntpd
        ntpd = subprocess.Popen([ntpd_path, "-f", "fuzz.conf", "-d", "-n"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ntpd.communicate(input=bytes(random_string, "utf-8"))


        # remove config and log file
        os.remove("fuzz.conf")
        os.remove("fuzz.log")


        # wait a bit
        time.sleep(1)


if __name__ == "__main__":
    main()
    