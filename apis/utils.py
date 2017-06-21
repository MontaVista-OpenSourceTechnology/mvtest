#! /usr/bin/env python


# Author: pkarat@mvista.com
# License: MIT
# (C) Copyright MontaVista Software, LLC 2016-2017. All rights reserved.


""" mvtest library with general purpose utility APIs"""


from colorlog import ColoredFormatter
from commands import getstatusoutput
import logging
import os
import paramiko
import pexpect
import re
import subprocess
import time


def custom_logger():
    COMMAND = 5
    EXIT_CODE = 15
    OUTPUT = 25
    PASS = 35
    FAIL = 45

    lnewlevel = [(COMMAND, 'COMMAND'), (EXIT_CODE, 'EXIT_CODE'),
                 (OUTPUT, 'OUTPUT'), (PASS, 'PASS'), (FAIL, 'FAIL')]
    for newlevel in lnewlevel:
        value, name = newlevel
        logging.addLevelName(value, name)
        setattr(logging, name, value)

    def command(self, *args, **kwargs):
        self.log(COMMAND, *args, **kwargs)
    logging.Logger.command = command

    def texit_code(self, *args, **kwargs):
        self.log(EXIT_CODE, *args, **kwargs)
    logging.Logger.texit_code = texit_code

    def output(self, *args, **kwargs):
        self.log(OUTPUT, *args, **kwargs)
    logging.Logger.output = output

    def tpass(self, *args, **kwargs):
        self.log(PASS, *args, **kwargs)
    logging.Logger.tpass = tpass

    def tfail(self, *args, **kwargs):
        self.log(FAIL, *args, **kwargs)
    logging.Logger.tfail = tfail

    logger = logging.getLogger('custom')
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.COMMAND)
    # create formatter
    formatter = ColoredFormatter(
        '%(log_color)s[%(levelname)s]%(reset)s %(message)s',
        datefmt=None,
        reset=True,
        log_colors={
            'COMMAND':      'purple',
            'EXIT_CODE':    'cyan',
            'INFO':         'cyan',
            'OUTPUT':       'blue',
            'PASS':         'green',
            'FAIL':         'red',
            'ERROR':        'red',
            'WARNING':      'yellow',
        }
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    logger.setLevel(logging.COMMAND)
    return logger


log = custom_logger()


def run_cmd(cmd, check_rc=True, wdir=None, stdout_arg=subprocess.PIPE,
            stdin_arg=None, shell=True, background=False, **kwargs):
    """
    Run a command, either interactively (default) or in background.


    Returns:
        None: on failure (non-zero return code) **OR**

        string: **NullOutput** or stripped command output on success **OR**

        Popen object: If background=True. Following methods & attributes
        could be used ::

                p = run_cmd(cmd, background=True)
                p.communicate()
                p.returncode
    Args:
        cmd (string): command to run.

        check_rc (bool): Default is True. False will not log command, output/
        errors.

        wdir (string): Run cmd from specificed directory.

        background (bool): Default is False. True returns Popen object. Run
        command in background. For usage see example below.

        stdout_arg: Default is *subprocess.PIPE*. Else *File descriptor*
        to output to a file.

        stdin_arg: Default is None. Progam's standard input.

        shell (bool): Default is True. Should be True for piped commands.
        See Ex 2: to know how to send piped commands.

        kwargs: optional arguments to be passed to Popen()

    Examples:
        Ex 1: To kill the parent and its child process and ensure no
        zombies are present. ::

            p = run_cmd(cmd, background=True, preexec_fn=os.setpgrp).
            do_something()
            do_something_else()
            os.kill(-p.pid, signal.SIGKILL)
                **OR**
            run_cmd('killall cmd')

        Ex 2: piped commands alternatively can be executed directly as ::

            run_cmd('cat sample | wc -l', shell=True)

    """
    stderr = subprocess.STDOUT
    p = None
    args = None
    if not isinstance(cmd, str):
        log.error("%s not in string format" % cmd)
        return None
    if check_rc:
        log.command(cmd)
    if not shell:
        args = cmd.split()
    else:
        args = cmd
    if wdir:
        try:
            origwdir = os.getcwd()
            os.chdir(wdir)
            p = subprocess.Popen(args, stdin=stdin_arg, stdout=stdout_arg,
                                 stderr=stderr, shell=shell, **kwargs)
            os.chdir(origwdir)
        except Exception as e:
            log.error(cmd + ' ' + str(e))
            os.chdir(origwdir)
            return None
    else:
        try:
            p = subprocess.Popen(args, stdin=stdin_arg, stdout=stdout_arg,
                                 stderr=stderr, shell=shell, **kwargs)
        except Exception as e:
            log.error(cmd + ' ' + str(e))
            return None

    if background:
        return p

    (out, _) = p.communicate()

    # log RC irrespective of output
    if check_rc:
        if out:
            log.texit_code(p.returncode)
        else:
            log.texit_code('%s\n' % p.returncode)

    if p.returncode != 0:
        if check_rc and out:
            log.error('%s\n' % out.strip())
        # Don't care about command output nor its return status
        # Just want to run the command without logging error
        return None
    elif not out:
        return 'NullOutput'
    else:
        if check_rc:
            log.output('%s\n' % out.strip())
        return out.strip()


def get_status_output(cmd, wdir=None):
    """
    Runs a command via the shell.

    Returns:
        tuple: (exit_code, text_output)
    """
    log.command(cmd)

    status = None
    output = None

    if wdir:
        origwdir = os.getcwd()
        os.chdir(wdir)
        status, output = getstatusoutput(cmd)
        os.chdir(origwdir)
    else:
        status, output = getstatusoutput(cmd)

    log.texit_code(status)

    if status != 0:
        if output:
            log.error('%s\n' % output.strip())
    else:
        if output:
            log.output('%s\n' % output.strip())

    return (status, output)


def check_kernel_configs(args, logging=True):
    """
    check if the given kernel config/s is enabled in the kernel.

    Returns:
        bool: On failure, missing kernel configs are listed as python
        list.

    Args:
        args (string or list): string for single kernel config **OR**
        a python list of kernel configs. See examples.

        logging (bool): logs errors if True. By default is True.

    Examples:
        ::

          1. check_kernel_configs('PREEMPT_RT_FULL')
          2. check_kernel_configs(['PREEMPT_RT_FULL', 'RELOCATABLE'])
          3. check_kernel_configs(['PREEMPT_RT_FULL=n', 'RELOCATABLE=m'])
          4. check_kernel_configs(['PREEMPT_RT_FULL=y', 'RELOCATABLE'])
    """
    configs = []
    not_present = []
    pattern = None
    if isinstance(args, str):
        configs = args.split()
    elif type(args) is list:
        configs = args
    else:
        log.error('%s not is string or list format' % args)
        return False
    out = run_cmd("zcat /proc/config.gz", check_rc=False)
    if not out:
        log.error('Failed to read /proc/config.gz')
        return False
    for conf in configs:
        if '=n' in conf:
            pattern = '%s is not set' % conf.split('=')[0]
            found = re.findall(r'%s' % pattern, out, re.M)
            if not found:
                pattern = pattern + "="
                found = re.findall(r'%s' % pattern, out, re.M)
                if found:
                    not_present.append(conf)
            continue
        elif '=' not in conf:
            pattern = '%s=' % conf
        elif '=' in conf:
            pattern = conf
        found = re.findall(r'%s' % pattern, out, re.M)
        if not found:
            not_present.append(conf)
    if not_present:
        if logging:
            log.error("List of missing kernel configs=%s" % not_present)
        return False
    return True


def run_stress(cpu=None, mem=None, membytes=None, io=None, timeout=None):
    """
    Impose cpu or memory or IO stress or all 3 at once in background.

    Returns:
        Popen: on success or *False* on failure.

    Args:
        cpu (int): Spawn N workers spinning on sqrt().

        mem (int): Spawn N workers spinning on malloc/free.

        io (int): Spawn N workers spinning on sync.

        membytes (string): malloc B bytes per vm worker.

        size can be B,K,M or G.

        timeout (string): Timeout after N seconds.

        time can be in  s, m, h, d, y
    """
    if not run_cmd('which stress'):
        return False
    cmd = 'stress'
    if cpu:
        cmd += ' --cpu %s' % cpu
    if mem:
        cmd += ' --vm %s' % mem
    if membytes:
        cmd += ' --vm-bytes %s' % membytes
    if io:
        cmd += ' --io %s' % io
    if timeout:
        cmd += ' --timeout %s' % timeout
    return run_cmd(cmd, background=True)


class RemoteMachine:
    """
    Returns:
        None: on failure
    Args:
        host (string): hostname or ipaddress of remote host.

        username (string): Default is root. If not root, specify username.

        password (string): Default is NULL. If not, specify password.
    """
    def __init__(self, host, username='root', password=''):
        self.host = host
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.host, username=username,
                                password=password, timeout=60)
        except:
            self.client = None

    def __del__(self):
        if self.client:
            self.client.close()

    def run_cmd(self, cmd):
        """
        Run a command in remote host.

        Returns:
            None: on failure (non-zero return code) **OR**

            string: **NullOutput** or stripped command output on success.

        Args:
            cmd (string) : command to run on remote host.

        Examples:
            ::

                remote = RemoteMachine('bogart')
                remote.run_cmd('uptime')

                remote = RemoteMachine('192.168.10.2')
                remote.run_cmd('uptime')
        """
        if not self.client:
            log.error('Failed connecting to\033[33m %s\033[0m' % self.host)
            return None

        log.command("\033[33m[%s]\033[0m %s" % (self.host, cmd))
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
        except:
            return None
        rc = stdout.channel.recv_exit_status()
        log.texit_code("\033[33m[%s]\033[0m %s" % (self.host, rc))
        if rc:
            log.error("\033[33m[%s]\033[0m %s" % (self.host,
                                                  stderr.read().strip()))
            return None
        out = stdout.read().strip()
        if out:
            log.output("\033[33m[%s]\033[0m %s" % (self.host, out))
            return out
        else:
            return 'NullOutput'

    def file_put(self, src, dst):
        """
        Transfer files from local target to remote machine.

        Returns::
            True: on success.

            False:  on failure

        Args:
            src : Absolute path of the file on target.

            dst : Absolute path of the file on remote

        Examples:
            ::

                remote = RemoteMachine('bogart')
                remote.file_put('/tmp/local_file', '/tmp/remote_file')
        """
        if not self.client:
            log.error('Failed connecting to\033[33m %s\033[0m' % self.host)
            return False

        try:
            ftp = self.client.open_sftp()
            log.info("copying %s to %s:%s" % (src, self.host, dst))
            ftp.put(src, dst)
            log.tpass('copied file successfully')
            return True
        except:
            log.error("copy %s to %s:%s failed" % (src, self.host, dst))
            return False

    def file_get(self, src, dst):
        """
        Transfer files from remote machine to local target.

        Returns:
            True: on success

            False:  on failure

        Args:
            src: Absolute path of the file on remote.

            dst: Absolute path of the file on local.

        Examples:
            ::

                remote = RemoteMachine('bogart')
                remote.file_get('/tmp/remote_file', '/tmp/local_file')
        """
        if not self.client:
            log.error('Failed connecting to\033[33m %s\033[0m' % self.host)
            return False

        try:
            ftp = self.client.open_sftp()
            log.info("copying %s:%s to %s" % (self.host, src, dst))
            ftp.get(src, dst)
            log.tpass('copied file successfully')
            return True
        except:
            log.error("copy %s:%s to %s failed" % (self.host, src, dst))
            return False


class ExpectShell(object):
    """
    Provides a set of APIs for interactive shell. Has four main methods

    1. connect:
        Spawns an expect shell

    2. run_cmd:
        Combines both expect send and match.

    3. match_group:
        Returns the matched regex pattern as tuples.

    4. terminate:
        Terminate the spawned process.
    """
    def __init__(self):
        self.shell = None

    def connect(self, cmd, timeout=30):
        """
        Returns:
            pexpect.spwan object: on success.

            False: on Failure

        Args:
            cmd (string): command to spawn.

            timeout (int): default 30 seconds.

        Examples:
            EX1::

                expect = ExpectShell()
                expect.connect('telnet shark 2305', timeout=60)

            Ex2::

                expect = ExpectShell()
                expect.connect('gdb a.out')
        """
        if not cmd:
            return False
        if self.shell is None:
            try:
                log.command("%s" % cmd)
                self.shell = pexpect.spawn(cmd, timeout=timeout,
                                           echo=False)
                return self.shell
            except pexpect.ExceptionPexpect:
                log.error("Failed to spwan %s " % cmd)
                return False

    def run_cmd(self, cmd, pattern, sleep=None, timeout=30):
        """
        Returns:
            Index into the pattern list: on success.

            If the pattern was not a list this returns index 0
            on a successful match.

            None: on Failure

        Args:
            cmd (string): command to run.

            pattern: StringType, or pexpect.EOF, a compiled re, or list.

            sleep (int): Default is None. Will sleep after sending command.

            timeout (int): default 30 seconds

        Examples:
            ::

                expect = ExpectShell()
                expect.connect('telnet shark 2305', timeout=60)
                index = expect.run_cmd('ls', pattern=['(*.py)', '*.sh'])
                assert index == 1 or index == 0
        """
        if cmd:
            log.command("%s" % cmd)
            self.shell.sendline(cmd)
        if sleep:
            log.info('sleeping for %s seconds' % sleep)
            time.sleep(sleep)
        try:
            log.info("PATTERN: \'%s\'" % pattern)
            self.index = self.shell.expect(pattern, timeout=timeout)
            if cmd:
                log.output(self.shell.before + self.shell.after)
            log.tpass("PATTERN FOUND: %s\n" % pattern)
            return self.index
        except:
            if cmd:
                log.output(self.shell.before)
            log.tfail('PATTERN NOT FOUND: %s\n' % pattern)
            return None

    def match_groups(self):
        """
        Returns:
            A tuple of matched groups.

        Examples:
            ::

                expect = ExpectShell()
                expect.connect('telnet shark 2305', timeout=60)
                index = expect.run_cmd('ls', pattern=['(*.py)', '*.sh'])
                assert index == 1 or index == 0
                log.info(expect.match_groups())
        """
        try:
            return self.shell.match.groups()
        except:
            log.error('Failed to match groups')
            return None

    def terminate(self):
        """
        Returns:
            True: on success.

            False: on failure.

        This forces a child process to terminate. It starts nicely with
        SIGHUP and SIGINT. If force is True then moves onto SIGKILL.
        """
        try:
            return self.shell.terminate(force=True)
        except:
            log.error('Failed to terminate')
            return False
