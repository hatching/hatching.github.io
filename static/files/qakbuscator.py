# Copyright (C) 2019 Hatching B.V.
# All rights reserved.

import os
import re
import sys

def patch_program(buf, match):
    size = match.end() - match.start()
    for i in range(size):
        buf[match.start() + i] = 0x90

def main(qbot_file):
    buf = bytearray(open(qbot_file, "rb").read())
    xor_pattern = re.compile("\x33.\x74\x02\xEB\xFA")

    # TODO Do the search only on .text section (or in the code section)
    # instead of the full binary.
    start = 0
    match = xor_pattern.search(buf, start)
    matches = []
    count = 0
    while match:
        count += 1
        start = match.start() + 1
        matches.append(match)
        patch_program(buf, match)
        match = xor_pattern.search(buf, start)

    open(qbot_file + ".deob", "wb").write(buf)

    print "[+] Binary successfully patched: %s" % (qbot_file + ".deob")
    print "\t - Found %d loops." % count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "[!] Invalid argument numbers. It must be 2"
        exit()

    if not os.path.exists(sys.argv[1]):
        print "[!] Provided file doesn't exist"
        exit()

    # Add more checks like the one to check if it's a PE FILE
    main(sys.argv[1])
