# cadasta-test

#### This repository contains Selenium UI automated test scripts that can be run against a cadasta server run on http://localhost:8000

First you have to create a user with the following credentials in your cadasta server

`username : cadasta-test-user-1
 password : XYZ#qwerty`

To install the dependencies :

`pip install -r requirements.pip`

To configure geckodriver (If you run the tests with firefox version > 48):

There are some test cases that require firefox version to be lower than 48. If you are running with newer version of firefox they will fail since the geckodriver still doesn't support the implementation of those test cases.

`Download from https://github.com/mozilla/geckodriver/releases
Unzip it and add to PATH variable`

To configure chromedriver (If you run the tests with chrome):

`Download from https://sites.google.com/a/chromium.org/chromedriver/downloads
Unzip it and add to PATH variable`

To run the tests :

`./runtests`
