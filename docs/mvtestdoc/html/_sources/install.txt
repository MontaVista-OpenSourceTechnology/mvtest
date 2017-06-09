.. install:

=======
Install
=======

Requirements
============

*python-pip* package **should be** availble on the target machine.

If not, download `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_.

Install it by running::

    $ python get-pip.py

This will install pip on the target machine.

Deploy
======


Follow either Basic Deployment or Isolated Deployment.

Basic Deployment::

    1. git clone https://github.com/premkarat/mvtest.git
    2. cd mvtest
    3. pip install -r requirements.txt
    4. export PYTHONDONTWRITEBYTECODE=1

To deploy mvtest in an isolated/virtual environment without conflicts with existing envrionment.

Isolated Deployment::

    1. pip install virtualenv
    2. git clone https://github.com/premkarat/mvtest.git
    3. cd mvtest
    4. virtualenv venv
    5. source venv/bin/activate
    6. pip install -r requirements.txt
    7. export PYTHONDONTWRITEBYTECODE=1


After running tests, to deactivate the virtual environment, run the following comand in venv::

    (venv):~$ deactivate
