#!/usr/bin/env python
import sys
from datetime import datetime
from telnetlib import Telnet


def wait_net_service(server, port, timeout=1):
    """
    Wait for network service to appear 
    @return: True of False, if timeout is None may return only True or throw unhandled network exception
    :type timeout: in seconds, if None or 0 wait forever
    :param port: port
    :param server: server address
    """
    first = datetime.now()
    while True:
        diff = datetime.now() - first
        # print(diff.total_seconds(), timeout)
        if diff.total_seconds() >= timeout:
            return False
        try:
            Telnet(server, port, 1)
            print("Connected after {} seconds".format(diff.total_seconds()))
            return True
        except Exception as e:
            # print(e)
            pass


if __name__ == '__main__':
    wait_net_service(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
