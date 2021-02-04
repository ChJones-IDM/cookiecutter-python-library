#!/usr/bin/env python3
# coding=utf-8

from __future__ import print_function
import os
import argparse
import re
from sys import exit
from subprocess import call


def get_argparser(parser=None):
    """Return default argparser object for command-line args for this script.

    Args:
            parser (argparser.ArgumentParser): the ArgumentParser object to add arguments to (useful for testing)

        Returns:
            argparser.ArgumentParser: ArgumentParser object w/ added arguments and config
    """
    if not parser:
        parser = argparse.ArgumentParser(description='')

    parser.add_argument('--commit-msg', required=True, help='Commit message.')
    parser.add_argument('--bump-type', help='Type: major, minor, patch, release, build')
    parser.add_argument('--auto-push', action='store_true', help='Push automatic version bump (when type specified).')
    parser.add_argument('--push-allowed', action='store_true', help='Allow push of bump version based on commit msg trigger.')
    parser.add_argument('--config-file', default='.bumpversion.cfg', help='Allow push of bump version based on commit msg trigger.')

    return parser


def main(args):
    """Main script function.

    Args:
        args: argparser parser.parse_args() object containing cmdline argument values as properties

    Returns:
        bool: success
    """

    # detect what type of version to bump based on commit message, default to 'patch'
    bump_type = args.bump_type
    push_commit = False

    if bump_type:
        push_commit = args.auto_push
    else:
        allowed_bump_types = ['major', 'minor', 'patch', 'release', 'build']
        bump_msg_match = re.match((r'\*\*\*BUMP (\w+)\*\*\*', args.commit_msg)

        if bump_msg_match:
            bump_msg_type = bump_msg_match.group(1).lower()
            if bump_msg_type in allowed:
                bump_type = bump_msg_type
        push_commit = args.push_allowed

    # bump version
    call(['pip', 'install', 'bump2version'])

    call(['bump2version', '--allow-dirty', '--config-file ' + args.config_file, bump_type])

    # push commit if allowed
    if push_commit:
        # git config
        call(['git', 'config', '--global', 'user.email', '"idm_bamboo_user@idmod.org"'])
        call(['git', 'config', '--global', 'user.name', '""BambooUser-IDM""'])
        call(['git', 'push'])

    return True


if __name__ == '__main__':
    """Run main function by default when run on cmdline (but not when imported as a library)  
    """
    parser = get_argparser()
    arguments = parser.parse_args()

    if not main(arguments):
        exit(1)
