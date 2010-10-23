#!/usr/bin/env python
# coding=utf-8

import sys
import tempfile
import xmlrpclib

from config import *

def remove_zim_header(zim):
    l = zim.readline()
    if not l.startswith('Content-Type:'):
        return False

    l = zim.readline()
    if not l.startswith('Wiki-Format:'):
        return False

    l = zim.readline()
    if not l.startswith('Creation-Date:'):
        return False

    return True

def convert_zim_to_wikidot(zim):
    if not remove_zim_header(zim):
        return

    i = 0
    content = zim.read()

    # FIXME: is there any string buffer in python?
    wikidot = ''

    headline = False
    link = False

    while i < len(content):
        if content[i] == '=':
            count = 1
            for x in range(i + 1, min(i + 6, len(content))):
                if content[x] != '=':
                    break
                count += 1

            i += count

            if count == 1:
                wikidot += '='
                continue

            if headline:
                if headline == 7 - count:
                    headline = False
                else:
                    # FIXME: How to handle unbalance headline?
                    assert False, 'unbalance headline tag'
            else:
                wikidot += '+' * headline
                headline = 7 - count

        elif content[i] == '~':
            if i + 1 < len(content) and content[i + 1] == '~':
                wikidot += '--'
                i += 2
            else:
                wikidot += content[i]
                i += 1

        elif content[i] == '[':
            # FIXME: implement link
            wikidot += content[i]
            i += 1

        elif content[i] == "'":
            # FIXME: implement quoted
            wikidot += content[i]
            i += 1

        elif content[i] == '^':
            # FIXME: implement subscript
            wikidot += content[i]
            i += 1

        elif content[i] == '}':
            # FIXME: implement superscript
            wikidot += content[i]
            i += 1

        else:
            wikidot += content[i]
            i += 1

    return wikidot

def main():
    doc_root = sys.argv[1]
    filename = sys.argv[2]

    all_config = get_all_config(doc_root)

    # FIXME: Let user select one of all_config. Now assume 0 is selected
    config = all_config[0]

    with open(filename, mode='rt') as zim:
        wikidot = convert_zim_to_wikidot(zim)


if __name__ == '__main__':
    main()
