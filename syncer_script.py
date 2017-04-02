#!/usr/bin/env python
import os
import sys
import pexpect
import argparse

from multiprocessing.pool import ThreadPool

from pexpect.exceptions import EOF


def pexpect_thread_command(items):
    pexpect_command(
        command=items[0],
        password=items[1]
    )


def pexpect_command(command, password):
    print("Started", command)
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
    print("END -", command)
    return proc.exitstatus


class Syncer(object):
    def sync(self, keys, sources, dest, dst_path, password, port=None):
        # create remote dir
        if dst_path:
            pexpect_command(
                command="ssh {destination} mkdir -p {dst_path}".format(
                    destination=dest,
                    dst_path=dst_path
                ),
                password=password,
            )

        # copy data
        commands = []
        for source in sources:
            if not os.path.exists(source):
                print("ERROR: Path {} does not exist".format(source))
                continue
            if port:
                # It means that we are connecting to the rsync daemon
                rsync_command = "rsync {keys} {source} rsync://{destination}:{port}/{dst_path}".format(
                    keys=keys,
                    source=source,
                    destination=dest,
                    dst_path=dst_path,
                    port=port
                )
            else:
                rsync_command = "rsync {keys} {source} {destination}:{dst_path}".format(
                    keys=keys,
                    source=source,
                    destination=dest,
                    dst_path=dst_path
                )

            commands.append((rsync_command, password,))

        tpool = ThreadPool(5)
        tpool.map(pexpect_thread_command, commands)

    def cml_sync(self):
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
            return 1

        sources = arguments.ITEMS[:-1]

        # Getting port
        user_port_host_parts = arguments.ITEMS[-1].split("@", 1)
        user = None
        port = None
        if len(user_port_host_parts) > 1:
            user_port_parts = user_port_host_parts[0].split(":", 1)
            if len(user_port_parts) > 1:
                try:
                    port = int(user_port_parts[1])
                except ValueError:
                    print("Port should be a number")
                    return 3
            user = user_port_parts[0]
            host_path = user_port_host_parts[1]
        else:
            host_path = user_port_host_parts[0]

        # Getting path
        host_path_parts = host_path.split(":", 1)
        host = host_path_parts[0]
        dst_path = ""
        if len(host_path_parts) > 1:
            dst_path = host_path_parts[1]

        # Combine destination
        if user:
            dst = "{user}@{host}".format(
                user=user,
                host=host
            )
        else:
            dst = host

        # Copy
        try:
            self.sync(keys=keys, sources=sources, dest=dst, dst_path=dst_path, password=arguments.password, port=port)
        except EOF:
            # split user@IP to display unreachable IP
            dst_split = dst.split("@", 1)
            if len(dst_split) == 1:
                dst_ip = dst_split[0]
            else:
                dst_ip = dst_split[1]
            print("Destination host {host} is unreachable".format(host=dst_ip))
            return 2

        return 0


if __name__ == "__main__":
    syncer = Syncer()
    sys.exit(syncer.cml_sync())
