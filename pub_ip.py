# -*- coding: UTF-8 -*-
import argparse

from telecom_toolkit import get_sysauth_cookie_value, get_pub_ip
from loguru import logger


def _main():
    parser = argparse.ArgumentParser(
        prog='telecom toolkit - pub ip',
        description='Read public ip address .'
    )
    parser.add_argument('-o', '--output_file')
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    args = parser.parse_args()
    sysauth = get_sysauth_cookie_value(args.username, args.password)
    logger.info(f"sysauth = {sysauth}")
    ip = get_pub_ip(sysauth_cookie=sysauth)
    logger.info(f"pub id = {ip}")
    with open(args.output_file, mode='w') as f:
        f.write(ip)


if __name__ == '__main__':
    _main()
