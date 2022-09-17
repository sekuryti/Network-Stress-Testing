# fuzzer for rsyslog

import os
import sys
import time
import random
import string
import subprocess


def main():
    if len(sys.argv) != 2:
        print("Usage: fuzz_rsyslog.py <path to rsyslog>")
        sys.exit(1)

    rsyslog_path = sys.argv[1]
    if not os.path.exists(rsyslog_path):
        print("rsyslog binary not found")
        sys.exit(1)

    while True:
        # generate random string
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))

        # create config file
        config_file = open("fuzz.conf", "w")
        config_file.write("module(load=\"imudp\")\n")
        config_file.write("input(type=\"imudp\" port=\"514\" ruleset=\"fuzz\")\n")
        config_file.write("ruleset(name=\"fuzz\") {\n")
        config_file.write("    action(type=\"omfile\" file=\"fuzz.log\")\n")
        config_file.write("}\n")
        config_file.close()

        # create log file
        log_file = open("fuzz.log", "w")
        log_file.close()

        # run rsyslog
        rsyslog = subprocess.Popen([rsyslog_path, "-f", "fuzz.conf", "-d", "-n"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rsyslog.communicate(input=bytes(random_string, "utf-8"))

        # check if log file is empty
        log_file = open("fuzz.log", "r")
        log_file_content = log_file.read()
        log_file.close()
        if len(log_file_content) == 0:
            print("rsyslog crashed")
            sys.exit(1)

        # remove config and log file
        os.remove("fuzz.conf")
        os.remove("fuzz.log")

        # wait a bit
        time.sleep(1)