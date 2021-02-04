#!/usr/bin/env python3
# coding=utf-8

from __future__ import print_function
import os
import argparse
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
    parser.add_argument('--auto-push-patch', action='store_true', help='Push automatic patch version bump.')
    parser.add_argument('--push-allowed', action='store_true', help='Allow push of bump version based on commit msg trigger.')

    return parser


def main(args):
    """Main script function.

    Args:
        args: argparser parser.parse_args() object containing cmdline argument values as properties

    Returns:
        bool: success
    """
    bump_type = None
    if '***BUMP MAJOR***' in args.commit_msg:
        bump_type = 'major'
    elif '***BUMP MINOR***' in args.commit_msg:
        bump_type = 'minor'
    elif '***BUMP PATCH***' in args.commit_msg:
        bump_type = 'patch'
    
    push_commit = False
    if bump_type:
        push_commit = args.push_allowed
    else:
        bump_type = 'patch'
        push_commit = args.auto_push_patch

    # bump version
    call(['bumpversion', '--allow-dirty', '--confi-file .bump_version.cfg', bump_type])

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
