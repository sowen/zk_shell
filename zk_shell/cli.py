""" entry point for CLI wrapper """

from __future__ import print_function

import argparse
import logging
import sys


from . import __version__
from .shell import Shell

try:
    raw_input
except NameError:
    raw_input = input


def get_params():
    """ get the cmdline params """
    parser = argparse.ArgumentParser()
    parser.add_argument("--connect-timeout",
                        type=int,
                        default=10,
                        help="ZK connect timeout")
    parser.add_argument("--run-once",
                        type=str,
                        default="",
                        help="Run a command non-interactively and exit")
    parser.add_argument("hosts",
                        nargs="*",
                        help="ZK hosts to connect")
    return parser.parse_args()


class CLI(object):
    """ the REPL """

    def run(self):
        """ parse params & loop forever """
        logging.basicConfig(level=logging.ERROR)

        params = get_params()
        shell = Shell(params.hosts,
                      params.connect_timeout,
                      setup_readline=params.run_once == "")

        if params.run_once != "":
            try:
                sys.exit(0 if shell.onecmd(params.run_once) == None else 1)
            except IOError:
                sys.exit(1)

        intro = "Welcome to zk-shell (%s)" % (__version__)
        first = True
        while True:
            try:
                shell.run(intro if first else None)
            except KeyboardInterrupt:
                done = raw_input("\nExit? (y|n) ")
                if done == "y":
                    break
            first = False
