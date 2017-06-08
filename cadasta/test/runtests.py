#!/usr/bin/env python

import argparse
import os
import sys
import pytest
from subprocess import Popen, DEVNULL


if __name__ == '__main__':
    # cadasta-test does not require Django
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        del os.environ['DJANGO_SETTINGS_MODULE']

    # Declare valid command-line arguments
    parser = argparse.ArgumentParser(
        description="Runs the Cadasta platform functional test suite.")
    parser.add_argument(
        '--host',
        default='http://localhost:8000',
        help=("HTTP host and optional port pointing to the Cadasta server to "
              "be tested (default: \"http://localhost:8000\")"),
    )
    parser.add_argument(
        '-w', '--webdriver',
        choices=['Chrome', 'Firefox'],
        default='Chrome',
        help="Selenium WebDriver to use",
    )
    parser.add_argument(
        'pyargs',
        nargs='*',
        help='optional arguments to be passed to pytest',
    )

    args = parser.parse_args()

    # Store host and webdriver into the environment
    os.environ['CADASTA_HOST'] = args.host
    os.environ['CADASTA_TEST_WEBDRIVER'] = args.webdriver

    # Ensure virtual frame buffer is running
    xvfb = Popen(["Xvfb", ":1"], stdout=DEVNULL, stderr=DEVNULL)
    os.environ['DISPLAY'] = ':1'

    # Run the tests using pytest
    result = pytest.main(args.pyargs)

    # Clean up and exit
    xvfb.terminate()
    sys.exit(result)
