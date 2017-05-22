#!/usr/bin/env python

import os
import sys
import pytest
from subprocess import Popen, DEVNULL


if __name__ == '__main__':
    # cadasta-test does not require Django
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        del os.environ['DJANGO_SETTINGS_MODULE']

    # Store optional cadasta host in the environment and extract optional
    # pytest arguments
    if len(sys.argv) >= 3 and sys.argv[1] == '--host':
        os.environ['CADASTA_HOST'] = sys.argv[2]
        pytest_args = sys.argv[3:]
    else:
        if 'CADASTA_HOST' in os.environ:
            del os.environ['CADASTA_HOST']
        pytest_args = sys.argv[1:]

    # Ensure virtual frame buffer is running
    xvfb = Popen(["Xvfb", ":1"], stdout=DEVNULL, stderr=DEVNULL)
    os.environ['DISPLAY'] = ':1'

    # Run the tests using pytest
    result = pytest.main(pytest_args)

    # Clean up and exit
    xvfb.terminate()
    sys.exit(result)
