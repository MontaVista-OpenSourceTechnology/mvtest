#!/usr/bin/env python
#
# Author: Prem Karat (pkarat@mvista.com)
# License: MIT
# (C) Copyright MontaVista Software, LLC 2016-2017. All rights reserved.


from apis.utils import check_kernel_configs
from apis.utils import run_cmd
import os
import pytest
import re
import sys


def pytest_configure(config):
    """Provide additional environment details to pytest-html report"""
    # add environment details to the pytest-html plugin
    msd_files = ['/boot/kenv.sh', '/etc/mvl7/conf/local-content.conf']
    msd_file = None
    for f in msd_files:
        if os.path.isfile(f):
            msd_file = f
            break

    msd = 'Unkown'
    msd_version = 'Unknown'
    msd_output = run_cmd('cat %s' % msd_file, check_rc=False)
    if msd_output:
        match = re.findall(r'MSD.*VERSION="(.*)"', msd_output, re.M)
        if match:
            msd_version = match[0]
        match = re.findall(r'.*MACHINE="(.*)"', msd_output, re.M)
        if match:
            msd = match[0]

    config._metadata['MSD'] = msd
    config._metadata['MSD Version'] = msd_version

    msd_release = run_cmd('cat /etc/mvl-release', check_rc=False)
    if not msd_release:
        msd_release = 'Unknown'
    config._metadata['MSD Release'] = msd_release

    hostname = run_cmd('hostname', check_rc=False)
    if not hostname:
        hostname = 'Unknown'
    config._metadata['Target'] = hostname

    kernel_preemption = 'Unknown'
    if check_kernel_configs('PREEMPT_RT_FULL', logging=False):
        kernel_preemption = 'PREEMPT_RT_FULL'
    elif check_kernel_configs('PREEMPT__LL', logging=False):
        kernel_preemption = 'PREEMPT__LL'
    elif check_kernel_configs('PREEMPT_NONE', logging=False):
        kernel_preemption = 'PREEMPT_NONE'
    config._metadata['Kernel Preemption'] = kernel_preemption

    uname_output = run_cmd('uname -mr', check_rc=False)
    kernel_release = 'Unknown'
    arch = 'Unknown'
    if uname_output:
        kernel_release, arch = uname_output.split()
    config._metadata['Kernel Release'] = kernel_release
    config._metadata['Arch'] = arch
    parameters = sys.argv
    if not parameters:
        test_name = 'Unknown'
    else:
        test_name = re.sub(r'.*test_','',''.join(filter(lambda x:'.py' in x, parameters)).replace(".py",""))
    if not test_name:
        test_name = 'Unknown'
    config._metadata['Test Name'] = test_name
