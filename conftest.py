#!/usr/bin/env python
#
# Author: Prem Karat (pkarat@mvista.com)
# License: MIT
# (C) Copyright MontaVista Software, LLC 2016-2019. All rights reserved.


from apis.utils import check_kernel_configs
from apis.utils import run_cmd
import re
import sys
import glob


def pytest_configure(config):
    """Provide additional environment details to pytest-html report"""
    # add environment details to the pytest-html plugin

    msd = 'Unknown'
    msd_version = 'Unknown'

    path = '/etc/mvl*/conf/emitted.inc'
    machine_file_list = glob.glob(path)

    if machine_file_list:

        machine_file = machine_file_list[0]

        machine_file_content = run_cmd('cat %s' % machine_file, check_rc=False)
        match = re.findall(r'''MACHINE_ARCH=\".*\"''', machine_file_content,
                           re.M)
        if match:
            machine = match[0]
            result = re.search('"(.*)"', machine)
            machine=result.group(1)
        else:
            machine = 'Unknown'

        machine = machine.replace('_','-')
        config._metadata['MACHINE'] = machine


        uname_output = run_cmd('uname -r', check_rc=False)
        match = re.findall('(\d+.\d+).*', uname_output, re.M)
        if match:
            kernel_version = match[0]
        else:
            kernel_version = 'Unknown'

        mvl_ver_output = run_cmd('cat /etc/mvl-version', check_rc=False)
        match = re.findall('(\d+.\d+).*', mvl_ver_output, re.M)
        if match:
            yocto_version = match[0]
            yocto_version = yocto_version.replace('7.0', '1.4')
        else:
            yocto_version = 'Unknown'

        kernel_yocto_version = '-'.join([kernel_version, yocto_version])
        config._metadata['Kernel-Yocto Version'] = kernel_yocto_version

        msd = '-'.join([machine, kernel_version, yocto_version])

        match = re.findall(r'MSD.*VERSION="(.*)"', machine_file_content, re.M)
        if match:
            msd_version = match[0]

    if msd_version == 'Unknown':

        path = '/etc/mvlcgx*/conf/emitted.inc'
        msd_ver_file_list = glob.glob(path)

        if msd_ver_file_list:
            msd_ver_file = msd_ver_file_list[0]
            msd_ver_file_output = run_cmd('cat %s' % msd_ver_file,
                                          check_rc=False)
            match = re.findall(r'MSD.*VERSION="(.*)"', msd_ver_file_output,
                               re.M)
            if match:
                msd_version = match[0]

    config._metadata['MSD Version'] = msd_version

    msd_release = run_cmd('cat /etc/mvl-release', check_rc=False)
    if not msd_release:
        msd_release = 'Unknown'
    config._metadata['MSD Release'] = msd_release

    if (re.findall(r'\d+',msd_release)):
        msd_release_version = re.findall(r'\d+',msd_release)[0]
        if( int(msd_release_version) >= 4):
            if( machine in ('ls1043ardb', 'ls1046afrwy', 'xilinx')):
                msd = 'Unknown'
    else:
        msd = 'Unknown'

    config._metadata['MSD'] = msd

    hostname = run_cmd('hostname', check_rc=False)
    if not hostname:
        hostname = 'Unknown'
    config._metadata['Target'] = hostname

    kernel_preemption = 'Unknown'
    if check_kernel_configs('PREEMPT_RT_FULL', logging=False):
        kernel_preemption = 'PREEMPT_RT_FULL'
    elif check_kernel_configs('PREEMPT_RT', logging=False):
        kernel_preemption = 'PREEMPT_RT'
    elif check_kernel_configs('PREEMPT__LL', logging=False):
        kernel_preemption = 'PREEMPT__LL'
    elif check_kernel_configs('PREEMPT_NONE', logging=False):
        kernel_preemption = 'PREEMPT_NONE'
    elif check_kernel_configs('PREEMPT_VOLUNTARY', logging=False):
        kernel_preemption = 'PREEMPT_VOLUNTARY'
    elif check_kernel_configs('PREEMPT', logging=False):
        kernel_preemption = 'PREEMPT'
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
        test_name = re.sub(r'.*test_', '', ''.join(
            filter(lambda x: '.py' in x, parameters)).replace(".py", ""))
    if not test_name:
        test_name = 'Unknown'
    config._metadata['Test Name'] = test_name
