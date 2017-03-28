#!/usr/bin/env python
import os
import sys
import pexpect
import argparse

from pexpect.exceptions import EOF


def pexpect_command(command, password):
    proc = pexpect.spawn(command)
    proc.logfile = sys.stdout
    index = 0
    while index != 1:
        index = proc.expect(["(yes/no)", "password:"])
        if index == 0:
            proc.sendline("yes")
        if index == 1:
            proc.sendline(password)
    proc.wait()
    return proc.exitstatus


def sync(keys, sources, dest, dst_path, password):
    # create remote dir
    if dst_path:
        pexpect_command(
            command="ssh {destination} mkdir -p {dst_path}".format(
                destination=dst,
                dst_path=dst_path
            ),
            password=password
        )

    # copy data
    for source in sources:
        if not os.path.exists(source):
            print("ERROR: Path {} does not exist".format(source))
            continue
        print("Copying {}".format(source))
        pexpect_command(
            command="rsync {keys} {source} {destination}:{dst_path}".format(
                keys=keys,
                source=source,
                destination=dest,
                dst_path=dst_path
            ),
            password=password
        )


if __name__ == "__main__":
    # Read and parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("ITEMS", help="Source and destination items", nargs="+")
    parser.add_argument("--password", help="destination password", required=True)
    parser.add_argument("-e", help="remote shell program")
    parser.add_argument("-P", action="store_const", help="partial progress", const="-P")
    parser.add_argument("--progress", action="store_const", help="partial progress", const="--progress")
    parser.add_argument("-a", action="store_const", help="archive", const="-a")
    parser.add_argument("-S", action="store_const", help="sparse", const="-S")
    parser.add_argument("-z", action="store_const", help="compress", const="-z")
    parser.add_argument("-q", action="store_const", help="quiet", const="-q")
    parser.add_argument("-v", action="store_const", help="verbose", const="-v")
    parser.add_argument("-i", action="store_const", help="output a change-summary for all updates", const="-i")
    arguments = parser.parse_args()

    print(arguments)

    # Parsing keys
    keys = []
    for key, value in vars(arguments).iteritems():
        # Skipping general items
        if key in ["ITEMS", "password"]:
            continue
        # Handling of the key - value arguments
        if key in ["e"]:
            if value:
                keys.append("-{k} '{v}'".format(k=key, v=value))
            continue
        # Handling of the boolean arguments
        if value:
            keys.append(value)

    # Join keys in one line
    keys = " ".join(keys)
    print(keys)

    # Sources and destination clarification
    if len(arguments.ITEMS) < 2:
        print("Source and destination are required")
        sys.exit(1)

    sources = arguments.ITEMS[:-1]

    full_dst = arguments.ITEMS[-1]
    dst_parts = full_dst.split(":", 1)

    dst = dst_parts[0]
    dst_path = ""
    if len(dst_parts) > 1:
        dst_path = dst_parts[1]

    # Copy
    try:
        sync(keys=keys, sources=sources, dest=dst, dst_path=dst_path, password=arguments.password)
        sys.exit(0)
    except EOF:
        # split user@IP to display unreachable IP
        dst_split = dst.split("@", 1)
        if len(dst_split) == 1:
            dst_ip = dst_split[0]
        else:
            dst_ip = dst_split[1]
        print("Destination host {host} is unreachable".format(host=dst_ip))
        sys.exit(2)
