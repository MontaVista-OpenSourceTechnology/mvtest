.. run:

=============
Running Tests
=============

Run tests from mvtest directory::

    py.test --html=<file-name.html> <options>

Example:

    ===  ==================================== ==============================
    #       command                            description
    ===  ==================================== ==============================
    1      py.test suites                       To run all tests
    2      py.test -m cg7                       To run all cge7 tests
    3      py.test -m cgx                       To run all cgx tests
    4      py.test suites/cgl                   To run all cgl tests
    5      py.test suites/dataplane             To run all dataplane tests
    6      py.test suites/foundation            To run all foundation tests
    7      py.test suites/iot                   To run all iot tests
    8      py.test suites/security              To run all security tests
    9      py.test --html=result.html suites    To save test run in result.html
    10     py.test -s suites                    To see entire test result in console
    ===  ==================================== ==============================

The --html option will save the test output in specified path in an html file. If this option is omitted then the test result as test-result.html in the mvtest directory.
