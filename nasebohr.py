#!/usr/bin/env python3

# Copyright 2020 Florian Bruhin (The Compiler) <me@the-compiler.org>
# Licensed under the MIT license, see LICENSE for details.

import argparse

import rich
import dns.resolver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name or names, separated by comma')
    parser.add_argument('rrtype', nargs='?', default='A',
                        help='RR type or types, separated by comma')
    parser.add_argument('server', nargs='?',
                        help='Nameserver to query')
    return parser.parse_args()


def do_query(resolver, name, rrtype):
    try:
        answer = resolver.query(name, rrtype)
    except dns.exception.DNSException as e:
        rich.print(f'[red]{e}[/red]')
        return

    for rr in answer:
        rich.print(f'[white]{name}[/white] [bright_black]{rrtype:4}[/bright_black] {rr}')


def main():
    args = parse_args()

    resolver = dns.resolver.Resolver(configure=args.server is None)
    if args.server is not None:
        resolver.nameservers = [args.server.lstrip('@')]

    for name in args.name.split(','):
        for rrtype in args.rrtype.split(','):
            do_query(resolver, name, rrtype)


if __name__ == '__main__':
    main()
