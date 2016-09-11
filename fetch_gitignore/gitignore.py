#! /usr/bin/env python2.7

'''
The fetch_gitignore library.
https://github.com/github/gitignore
'''

import re
import json
import base64

import requests

# API endpoint.
GITHUB = 'https://api.github.com/repos/github/gitignore/contents'


def http_debug(response):
    '''
    Print the HTTP request/response debug log.
    '''
    print 'http-request\n{0}\n'.format('-' * len('http-request'))
    print 'url ({0}): {1}'.format(response.request.method,
                                  response.request.url)
    print 'request-headers:'
    print json.dumps(dict(response.request.headers), indent=4)
    if response.request.method != 'GET':
        if response.request.body:
            print 'request-payload:'
            try:
                print json.dumps(json.loads(response.request.body), indent=4)
            except (KeyError, ValueError):
                pass
    print '\nhttp-response\n{0}\n'.format('-' * len('http-response'))
    print 'status-code: {0} {1}'.format(response.status_code, response.reason)
    print 'url: {0}'.format(response.url)
    print 'time-elapsed: {0}s'.format(response.elapsed.total_seconds())
    print 'response-headers:'
    print json.dumps(dict(response.headers), indent=4)
    print 'response-content:'
    print None if response.content is '' else json.dumps(response.json(),
                                                         indent=4)


def github(url, token=None, debug=False):
    '''
    A common method to fetch responses from the GitHub API.
    '''
    if url:
        token = (token.strip(), '') if token else None
        try:
            response = requests.get(url, auth=token, allow_redirects=True)
            if debug:
                http_debug(response)
            if response.status_code >= 200 and response.status_code < 400:
                return response.json()
        except (requests.exceptions.RequestException, ValueError):
            pass

    return {}


def fetch(which, thing, token=None, debug=False):
    '''
    Do patter matching against which (a list).
    '''
    name = re.sub('.gitignore', '', thing['name']).strip()

    for each in which:
        if (re.search(re.escape(each), name, re.I) and
                thing['type'] == 'file' and len(each) == len(name)):
            if debug:
                print ('\n\n[fetch] {0} from \'{1}\'').format(name.lower(),
                                                              thing['url'])
            raw = github(url=thing['url'], token=token, debug=debug)
            return (name.lower(), base64.decodestring(raw['content']))


def ignore(which, token=None, debug=False):
    '''
    Fetch all files in a directory; recursion level: 1. (except for Global)
    Global also has a list of common .gitignore files.
    '''
    git_ignores = []

    if debug:
        print '[fetch] \'{0}\''.format(GITHUB)

    for thing in github(url=GITHUB, token=token, debug=debug):
        try:
            if thing['name'] == 'Global' and thing['type'] == 'dir':
                level = github(url=thing['url'], token=token)
                for inner in level:
                    git_ignore = fetch(which, inner, token, debug)
                    if git_ignore:
                        git_ignores.append(git_ignore)
            elif thing['type'] == 'file':
                git_ignore = fetch(which, thing, token, debug)
                if git_ignore:
                    git_ignores.append(git_ignore)

        except (ValueError, KeyError, TypeError, IndexError):
            continue

    return git_ignores
