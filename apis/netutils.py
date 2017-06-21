#! /usr/bin/env python


# Author: pkarat@mvista.com
# License: MIT
# (C) Copyright MontaVista Software, LLC 2016-2017. All rights reserved.


""" Utilities for tests under suites/net."""


from utils import log
from utils import run_cmd
import socket


def ping(ripaddr=None, count=None):
    """
    Ping remote machine with N number of packets.

    Args:
        ripaddr (string): Remote IPv4 address.

        count (string): Number of packets to be sent.

    Returns:
        bool: True on 0% packet loss or False on partial/100% loss. **OR**

        Popen object: If count is not specified.
    """
    cmd = 'ping'
    if not ripaddr:
        log.error('No remote ipaddr specified')
        return False
    cmd = cmd + ' ' + ripaddr
    if count:
        cmd = cmd + ' -c %s' % count
        out = run_cmd(cmd)
        if out:
            if '0% packet loss' in out:
                return True
            else:
                log.error('packet loss found.\n%s' % out)
                return False
        else:
            log.error('ping failed.\n%s' % out)
            return False
    else:
        return run_cmd(cmd, background=True)


def getip():
    "Return local ip address"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    s.close()
    return ip
