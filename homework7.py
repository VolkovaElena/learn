#!/usr/bin/env python
import pexpect
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='What to copy', required=True)
    parser.add_argument('--dst', help='Where to copy (user@IP)', required=True)
    parser.add_argument('--password', help='destination password', required=True)
    parser.add_argument('-P', action='store_const', help='partial progress', const='P')
    parser.add_argument('-a', action='store_const', help='archive', const='a')
    parser.add_argument('-S', action='store_const', help='sparse', const='S')
    parser.add_argument('-z', action='store_const', help='compress', const='z')
    parser.add_argument('-q', action='store_const', help='quiet', const='q')
    arguments = parser.parse_args()

    keys = []
    for key in "PaSzq":
        if getattr(arguments, key, None):
            keys.append(key)
    if keys:
        keys = "".join(["-"] + keys)
    else:
        keys = ""
    print(keys)

    print(arguments)

    rsync = pexpect.spawn("rsync {keys} {source} {destination}:".format(
        keys=keys,
        source=arguments.source,
        destination=arguments.dst
    ))

    index = 0
    while index != 1:
        index = rsync.expect(["(yes/no)", "password:"])
        if index == 0:
            rsync.sendline("yes")
        if index == 1:
            rsync.sendline(arguments.password)

    rsync.wait()
