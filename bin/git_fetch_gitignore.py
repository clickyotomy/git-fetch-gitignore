#! /usr/bin/env python2.7

'''
This is an executable script with command line options to fetch .gitignore
files from GitHub.
'''

import os
import sys
from argparse import ArgumentParser

try:
    import imp
    imp.find_module('fetch_gitignore')
except ImportError:
    PATH = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(PATH)))

from fetch_gitignore import gitignore


def fetch(which, token=None, path='./.gitignore', mode='a', debug=False):
    '''
    Call the library function, get the file, stitch them together.
    '''
    try:
        ignore_files = gitignore.ignore(which, token, debug)

        if len(ignore_files) <= 0:
            return

        with open(path, mode) as _gitignore:
            header = ('\n# Generated automcatically using '
                      'git-fetch-gitignore.\n')
            _gitignore.write(header)
            if debug:
                print '[write] \'{0}\''.format(path)
            for _what, _file in ignore_files:
                _gitignore.write(''.join(['\n# -- ', _what,
                                          '.gitignore', ' -- \n\n']))
                _gitignore.write(''.join([_file, '\n']))
    except KeyboardInterrupt:
        print ''

    return


def main():
    '''
    Validate arguments, get the .gitignore file(s).
    '''
    description = 'git-fetch-gitignore: Fetch .gitignore files from GitHub.'
    fetch_help = 'list of .gitignore files to fetch'
    overwrite_help = ('over-writes the existing .gitignore file if set, '
                      'appends to it, by default')
    write_to_help = 'file to output; defaults to ./.gitignore'
    token_help = 'a file containing the GitHub personal access token'

    parser = ArgumentParser(description=description)
    parser.add_argument('-l', '--list', help=fetch_help, nargs='+',
                        metavar=('FILE'), required=True)
    parser.add_argument('-w', '--write-to', help=write_to_help,
                        default='./.gitignore', metavar=('FILE'))
    parser.add_argument('-o', '--over-write', help=overwrite_help,
                        default=False, action='store_true')
    parser.add_argument('-t', '--token-file', help=token_help)
    parser.add_argument('-d', '--debug', help='enable debugging',
                        default=False, action='store_true')

    args = vars(parser.parse_args())

    token = None
    mode = 'w' if args['over_write'] else 'a'
    args['list'] = [_.lower() for _ in args['list']]

    if args['token_file']:
        with open(args['token_file'], 'r') as _token_file:
            token = _token_file.read().strip()

    fetch(which=args['list'], token=token, path=args['write_to'], mode=mode,
          debug=args['debug'])


if __name__ == '__main__':
    main()
