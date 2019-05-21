About mvtest
============

mvtest is an open-source automated test suite based on pytest framework to perform a full-fledged QA on MontaVista Linux Distribution::

    © Copyright MontaVista Software, LLC 2016-2019. All rights reserved.

    Licensed under the MIT license

mvtest has following advantages

* easy to deploy and run tests. Exaclty takes 4 commands to deploy and run tests.
* maintenance-free test framework. mvtest is based on [pytest](http://pytest.org/latest/>). pytest is a stable and well-maintained open-source test framework.
* easy to distrbute to Partners and Customers' as its based on MIT license.
* provides easy no-boilerplate testing. Helps developers, QA and support engineers to develop tests quickly with no-frills.
* scalable from unit testing to system level and integration testing.
* mvtest, based on pytest, is easy to learn with rich documentation available online. Check out learning resources.
* simple yet powerful!

Install
=======

Requirements
============

python-pip package should be availble on the target machine.

If not, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Install it by running::

    $ python get-pip.py

This will install pip on the target machine.

Deploy
======

Basic steps::

    1. git clone https://github.com/MontaVista-OpenSourceTechnology/mvtest.git
    2. cd mvtest
    3. pip install -r requirements.txt
    4. export PYTHONDONTWRITEBYTECODE=1

To deploy mvtest in an isolated/virtual environment without conflicts with existing envrionment::

    1. pip install virtualenv
    2. git clone https://github.com/MontaVista-OpenSourceTechnology/mvtest.git
    3. cd mvtest
    4. virtualenv venv
    5. source venv/bin/activate
    6. pip install -r requirements.txt
    7. export PYTHONDONTWRITEBYTECODE=1

After running tests, to deactivate the virtual environment, run the following comand in venv::

    (venv):~$ deactivate

**NOTE**:  If setup fails to install python cyrptography module, ensure, libssl-dev libffi-dev python-dev libraries are installed on the system.

Running Tests
=============

Run tests from mvtest directory::

    pytest --html=<file-name.html> <options>

| command | description |
| ------- | ----------- |
| pytest suites | To run all tests |
| pytest -m cg7 | To run all cge7 tests |
| pytest -m cgx | To run all cgx tests |
| pytest suites/cgl | To run all cgl tests |
| pytest suites/dataplane | To run all dataplane tests |
| pytest suites/foundation | To run all foundation tests |
| pytest suites/iot | To run all iot tests |
| pytest suites/security | To run all security tests |
| pytest --html=result.html suites | To save test run in result.html |
| pytest -s suites | To see entire test result in console |

The --html option will save the test output in specified path in an html file.
If this option is omitted then the test result will be stored as test-result.html.

Test Results
============

Test results are available in 2 formats::

    1. html log (Default, under mvtest/test-result.html)
        OR
    2. console log

console log can be obtained by using option '-s' with pytest::

    pytest -s <option>

mvtest documentation
====================

mvtest documentation is hosted in [github pages](https://montavista-opensourcetechnology.github.io/mvtest/home.html)

