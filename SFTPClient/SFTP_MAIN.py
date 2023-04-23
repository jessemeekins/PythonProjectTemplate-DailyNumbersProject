#!/bin/bash/python310
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more information.
"""

import argparse
from SFTP_Client import sftp_main


title = """
  ____ _____ _____ _____ 
 / ___|_   _|_   _| ____|
| |     | |   | | |  _|  
| |___  | |   | | | |___ 
 \____| |_|   |_| |_____|
"""

test = """
 _______   _______   _______   _______
|       | |       | |       | |       |
|_     _| |    ___| |  _____| |_     _|
  |   |   |   |___  | |_____    |   |  
  |   |   |    ___| |_____  |   |   |  
  |   |   |   |___   _____| |   |   |  
  |___|   |_______| |_______|   |___|  
"""

# Brief description
description = "[*] This Python script allows you to transfer files securely over SFTP."

# Create the argument parser
parser = argparse.ArgumentParser(description=description)

# Define the arguments
parser.add_argument("-devf", "--DEV_FULL", action="store_true", help="Transfer full roster will all codes in the directory")
parser.add_argument("-f", "--PROD_FULL", action="store_true", help="Transfer full roster will all codes in the directory")
parser.add_argument("-deva", "--DEV_PAR", action="store_true", help="Transfer roster with working codes only")
parser.add_argument("-a", "--PROD_PAR", action="store_true", help="Transfer roster with working codes only")

# Parse the arguments
args = parser.parse_args()

# Print the title and description
print(title)
print()
print(description)
print()
# Print which arguments the script accepts
print("[*] When pulling the roster data, remember that theshift ends at 0659. If run at 0659, 'yesterdays' roster will be downaloaded")
print()
print("[*] This script accepts the following arguments:")
print("[*] -f: 'FULL' roster export including all paycodes scheduled for today.")
print("[*] -a: 'PAR' roster export for working codes only on the current shift.")
print()

# Print the arguments passed
print("[*] The following arguments were passed:")
if args.DEV_FULL:
    print(test)
    print("[*] The 'DEV_FULL' roster report is now being downlaoded...")
    sftp_main("DEV_FULL")
if args.PROD_FULL:
    print("[*] The 'PROD_FULL' roster report is now being downlaoded...")
    sftp_main("PROD_FULL")
if args.DEV_PAR:
    print(test)
    print("[*] The 'DEV_PAR' radio roster report is now being downlaoded...")
    sftp_main("DEV_PAR")
if args.PROD_PAR:
    print("[*] The 'PAR' radio roster report is now being downlaoded...")
    sftp_main("PROD_PAR")



