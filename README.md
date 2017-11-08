# cadasta-test

The **Cadasta Functional Test Suite** is a separate project that provides automated user-interface tests to verify the functionality of the Cadasta Platform from the point of view of a user using a web browser. The test suite uses [Selenium](http://docs.seleniumhq.org/) as the main technology for writing automated tests. These tests are written in Python using [Selenium bindings](http://selenium-python.readthedocs.io/). Selenium, in cooperation with the browser software companies, provides various WebDrivers that interface with a real browser like Firefox or Chrome, or a headless browser like [PhantomJS](http://phantomjs.org/). The tests instruct the WebDriver which then controls user interactions on the browser such as entering text into form fields or clicking buttons.

For more information on the test suite architecture and how to run functional tests locally in the development VM, please refer to the following wiki pages:

* [Functional test architecture](https://github.com/Cadasta/cadasta-platform/wiki/Functional-test-architecture)
* [Running functional tests](https://github.com/Cadasta/cadasta-platform/wiki/Running-functional-tests)
