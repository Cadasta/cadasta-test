# cadasta-test
### Cadasta Test is for test scripts related to automated testing. This repository contains Selenium UI Automated Tests that can be run against a cadasta server run on http://localhost:8000

First you have to create a user with the following credentials in your cadasta server
`username : cadasta-test-user-1
 password : XYZ#qwerty`

To install the dependencies :
	`pip install -r requirements.pip`

To configure geckodriver :
	Download from https://github.com/mozilla/geckodriver/releases
	Unzip it and add to PATH variable

To run the tests :
       `./manage.py test selenium_tests`
