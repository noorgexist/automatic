#!/usr/bin/env python3

import socket
import logging
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('domain_name', help='- domain name to get ipv6 address')
parser.add_argument('upstream_file', help='- upstream file in which you will write changes')
parser.add_argument('logfile', help='- logfile for logs')
args = parser.parse_args()

logfile = args.logfile
upstream_file = args.upstream_file
domain_name = args.domain_name

switch_ip_logger = logging.getLogger('switch_ip')
switch_ip_logger.setLevel(logging.DEBUG)
switch_ip_logger_fh = logging.FileHandler(logfile)
switch_ip_logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
switch_ip_logger_fh.setFormatter(switch_ip_logger_formatter)
switch_ip_logger.addHandler(switch_ip_logger_fh)

with open(upstream_file, 'r+') as upstream:
    try:
        iplist = socket.getaddrinfo(domain_name, 443, socket.AF_INET6, socket.SOCK_STREAM)
    except socket.gaierror:
        switch_ip_logger.critical('App failed with socket.gaierror')
        sys.exit()
    u = upstream.read()
    for ip in iplist:
        if not ip[4][0] in u:
            upstream.write('server [{}]:443;\n'.format(ip[4][0]))
#            subprocess.run(['nginx', '-s', 'reload'])
            switch_ip_logger.info('Address was changed to {}'.format(ip[4][0]))
