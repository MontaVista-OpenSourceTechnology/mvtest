.. run:

=============
Running Tests
=============

Run tests from mvtest directory::

    pytest --html=<file-name.html> <options>

Example:

    ===  ==================================== ==============================
    #       command                            description
    ===  ==================================== ==============================
    1      pytest suites                       To run all tests
    2      pytest -m cg7                       To run all cge7 tests
    3      pytest -m cgx                       To run all cgx tests
    4      pytest suites/cgl                   To run all cgl tests
    5      pytest suites/dataplane             To run all dataplane tests
    6      pytest suites/foundation            To run all foundation tests
    7      pytest suites/iot                   To run all iot tests
    8      pytest suites/security              To run all security tests
    9      pytest --html=result.html suites    To save test run in result.html
    10     pytest -s suites                    To see entire test result in console
    ===  ==================================== ==============================

The --html option will save the test output in specified path in an html file. If this option is omitted then the test result as test-result.html in the mvtest directory.
