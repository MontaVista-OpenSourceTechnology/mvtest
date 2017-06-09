#!/usr/bin/env python
#
# Author: Prem Karat (pkarat@mvista.com)
# License: MIT


from apis.utils import (ExpectShell,
                        get_status_output,
                        RemoteMachine,
                        run_cmd,
                        log)
import pytest
import time


def test_run_cmd():
    """
    This is a sample test to test run_cmd() API.
    """
    out = run_cmd('uname -a')
    assert 'Linux' in out


def test_remote_connectivity():
    """
    This is a sample test to test RemoteMachine() API.
    """
    remoteserverip = ''
    remote_user = 'root'
    remote_passwd = ''
    if not remoteserverip:
        pytest.skip('remote server ip not specified')
    remote = RemoteMachine(remoteserverip, remote_user, remote_passwd)
    out = remote.run_cmd('uname -a')
    assert 'Linux' in out


def test_get_status_output():
    """
    This is a sample test to test get_status_output() API.
    """
    exit_code, output = get_status_output('ls')
    assert exit_code == 0
    assert output


def test_expect_shell(request):
    """
    This is a sample test to test ExpectShell() API. Open up a telnet
    session and run expect commands.
    """
    ipaddr = ''
    port = ''

    if not ipaddr:
        pytest.skip('ip address not specified for telnet session')
    if not port:
        pytest.skip('port not specified for telnet session')

    expect = ExpectShell()

    def cleanup():
        log.info('Terminating child')
        expect.terminate()

    request.addfinalizer(cleanup)

    assert expect.connect('telnet %s %s' % (ipaddr, port), timeout=30)
    index = expect.run_cmd('', pattern="Escape character is \'\^\]\'\.")
    assert index == 0
    time.sleep(5)
    index = expect.run_cmd('\n', 'login\:', sleep=5, timeout=3)
    assert index == 0
    index = expect.run_cmd('root', 'root', timeout=3)
    assert index == 0
    index = expect.run_cmd('ls', "crap.py", timeout=3)
    assert index is None
    index = expect.run_cmd('ls', "mvtest", timeout=3)
    assert index == 0


def test_platform_is_ppc():
    """
    This is a sample negative test to show failure.
    """
    out = run_cmd('uname -a')
    assert 'ppc' in out
