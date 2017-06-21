#! /usr/bin/env python


# Author: pkarat@mvista.com
# License: MIT
# (C) Copyright MontaVista Software, LLC 2016-2017. All rights reserved.


"""Utilites for tests under suites/kernel tests."""


from utils import log
from utils import run_cmd


def get_nr_cpus():
    """
    Return number of available online cpus.

    Returns:
        int: Number of online cpus from /proc/cpuinfo
    """
    nr_cpus = run_cmd('grep processor /proc/cpuinfo | wc -l', check_rc=False)
    if nr_cpus:
        return int(nr_cpus)
    else:
        # something is wrong here. Atleast there should be 1 cpu online
        return 0


def get_online_cpus():
    """
    Returns a list of online cpus from /sys/devices/system/cpu/online.

    Returns:
        list: cpu0 is not included as its expected be online.
    """
    lonline_cpus = []
    out = run_cmd('cat /sys/devices/system/cpu/online', check_rc=False)
    if not out:
        log.error('/sys/devices/system/cpu/online shows null output')
        return []
    lout = out.split(',')
    for cpus in lout:
        if '-' in cpus:
            start, end = cpus.split('-')
            if start == '0':
                start = '1'
            lcpus = range(int(start), int(end) + 1)
            lcpus = [str(i) for i in lcpus]
            lonline_cpus = lonline_cpus + lcpus
        elif cpus is not '0':
            lonline_cpus.append(cpus)
    return lonline_cpus


def make_cpu_online(cpus=None, online=True):
    """
    Enable the list of cpus online.

    Returns:
        bool: True on success. False on failure.

    Examples::

        make_cpu_online('5') # make cpu5 online
        make_cpu_online(['2', '5', '7']) # make cpu2,5,7 online
        make_cpu_online(5)
    """
    if not cpus:
        log.error('No cpus sepcified')
        return False
    value = 1
    if not online:
        value = 0
    sysfs_online = ''
    if isinstance(cpus, list):
        fail_cpus = []
        for cpu in cpus:
            if str(cpu) == '0':
                continue
            sysfs_online = '/sys/devices/system/cpu/cpu%s/online' % cpu
            cmd = 'echo %s > %s' % (value, sysfs_online)
            if not run_cmd(cmd):
                fail_cpus.append(cpu)
        if fail_cpus:
            log.error('CPU online operation failed on cpus = %s'
                      % fail_cpus)
            return False
        return True
    else:
        if str(cpus) == '0':
            log.error('Invalid operation for cpu0')
            return False
        sysfs_online = '/sys/devices/system/cpu/cpu%s/online' % cpus
        cmd = 'echo %s > %s' % (value, sysfs_online)
        if not run_cmd(cmd):
            return False
        return True


def make_cpu_offline(cpus=None):
    """
    Enable the list of cpus online.

    Returns:
        bool: True on success. False on failure.

    Examples::

        make_cpu_offline('5')
        make_cpu_offline(['2', '5', '7'])
        make_cpu_offline(5)
    """
    return make_cpu_online(cpus, online=False)
