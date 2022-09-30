""" Simple object for command line interface """
import argparse

class Cmdline:
    """ Cmdline Object """
    def __init__(self):
        """ Initialize Cmdline object """
        # set arg options
        self.parser = argparse.ArgumentParser(
            description="Argument list", add_help=True,
        )
        # add arguments here
        #parser.add_argument('-d', '--debug', action='store_true', dest='debug')
        self.args = self.parser.parse_args()
