#!/usr/bin/python3
"""
SSOF-Automation

Overview:
    Bare-bones structure of application
"""
import logging 

from local.cmdline import Cmdline
from local.env import LOG_LEVEL


def main():
    """
    def main()

    Overview:
        Lorem ipsum sit amet
    """

if __name__ == "__main__":
    # init settings
    logging.basicConfig(level=LOG_LEVEL)
    logging.getLogger().setLevel(LOG_LEVEL)
    # initialize program
    logging.info("Initializing %s ...", __name__)
    main()
