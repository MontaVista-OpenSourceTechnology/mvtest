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

    For pip3::

    $ python3 get-pip.py

This will install pip on the target machine.

Deploy
======


Follow either Basic Deployment or Isolated Deployment.

Basic Deployment::

    1. git clone https://github.com/MontaVista-OpenSourceTechnology/mvtest.git
    2. cd mvtest
    3. For CGE7: pip install certifi
    4. pip install -r requirements.txt
    5. export PYTHONDONTWRITEBYTECODE=1

To deploy mvtest in an isolated/virtual environment without conflicts with existing envrionment.

Isolated Deployment::

    1. pip install virtualenv
    2. git clone https://github.com/MontaVista-OpenSourceTechnology/mvtest.git
    3. cd mvtest
    4. virtualenv venv
    5. source venv/bin/activate
    6. For CGE7: pip install certifi
    7. pip install -r requirements.txt
    8. export PYTHONDONTWRITEBYTECODE=1



Isolated Deployment (python 3)::

	1. git clone https://github.com/MontaVista-OpenSourceTechnology/mvtest.git
	2. cd mvtest
	3. python3 -m venv venv
	4. source venv/bin/activate
	5. For CGE7: pip install certifi
	6. pip3 install -r requirements.txt
	7. export PYTHONDONTWRITEBYTECODE=1

After running tests, to deactivate the virtual environment, run the following comand in venv::

    (venv):~$ deactivate
