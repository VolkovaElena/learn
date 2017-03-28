#!/usr/bin/env python
import os
import sys
import pexpect
import argparse


def pexpect_command(command, password):
    proc = pexpect.spawn(command)
    proc.logfile = sys.stdout
    index = 0
    while index != 1:
        index = proc.expect(['(yes/no)', 'password:'])
        if index == 0:
            proc.sendline('yes')
        if index == 1:
            proc.sendline(password)
    proc.wait()
    return proc.exitstatus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='What to copy', required=True, nargs='+')
    parser.add_argument('--dst', help='Where to copy (user@IP)', required=True)
    parser.add_argument('--dst-path', help='Destination folder on remote host', required=False, default="")
    parser.add_argument('--password', help='destination password', required=True)
    parser.add_argument('-P', action='store_const', help='partial progress', const='P')
    parser.add_argument('-a', action='store_const', help='archive', const='a')
    parser.add_argument('-S', action='store_const', help='sparse', const='S')
    parser.add_argument('-z', action='store_const', help='compress', const='z')
    parser.add_argument('-q', action='store_const', help='quiet', const='q')
    parser.add_argument('-v', action='store_const', help='verbose', const='v')
    arguments = parser.parse_args()

    keys = []
    for key in 'PaSzq':
        if getattr(arguments, key, None):
            keys.append(key)
    if keys:
        keys = ''.join(['-'] + keys)
    else:
        keys = ''

    # create remote dir
    if arguments.dst_path:
        pexpect_command(
            command='ssh {destination} mkdir -p {dst_path}'.format(
                destination=arguments.dst,
                dst_path=arguments.dst_path
            ),
            password=arguments.password
        )

    # copy data
    for source in arguments.source:
        if not os.path.exists(source):
            print("ERROR: Path {} does not exist".format(source))
            continue
        print("Copying {}".format(source))
        pexpect_command(
            command='rsync {keys} {source} {destination}:{dst_path}'.format(
                keys=keys,
                source=source,
                destination=arguments.dst,
                dst_path=arguments.dst_path
            ),
            password=arguments.password
        )


if __name__ == '__main__':
    main()
