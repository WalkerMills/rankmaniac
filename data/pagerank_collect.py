#! /usr/bin/env python2

from __future__ import with_statement

import os
import subprocess
import sys

DATA_DIR = "tmp"
PREFIX = DATA_DIR + "/part-"
REDUCER = "./pagerank_reduce.py"

def main(argv):
    for line in sys.stdin:
        line = line.rstrip()
        key, _, value = line.partition("\t")

        with open(PREFIX + key, "a") as f:
            f.write(line + "\n")

    for filename in os.listdir(DATA_DIR):
        local_path = "{}/{}".format(DATA_DIR, filename)
        with open(local_path, "r") as f:
            proc = subprocess.Popen(REDUCER, stdin=subprocess.PIPE)
            proc.communicate(''.join(f.readlines()))
        os.remove(local_path)

if __name__ == "__main__":
    main(sys.argv)