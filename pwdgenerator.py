#! /usr/bin/python3

import argparse
from multiprocessing.dummy import current_process
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PlatformConstants import USER_DIR
from custom_modules.PatternConstants import has_ext as he
from custom_modules.PasswordGenerator import generate_password_thread as gpt
from custom_modules.FileOperator import save_new_file as snf, delete_file as df
from custom_modules.FileValidator import file_exists as fe

cus = cms["custom"]
msg = None
desc = "This program will generate a random string of characters"
epil = "The string is generated from a combination of digits, upper and lower case letters and punctuation characters"
vers = "%prog 0.1"
pwd = ""
default_name = "generated-password.txt"
verbose = False
save_to_file = False


def exit_prog(exit_code=0):
    sys.exit(exit_code)


def error_handler(*args):
    cus = cms["custom"]
    e_msg_header = cus(255, 120, 120, "Error:")
    e_msg_body = cus(255, 255, 255, "{}".format(args[0]))
    e_msg = "\n\t{} {}\n".format(e_msg_header, e_msg_body)
    print("{}".format(e_msg))
    exit_prog()


parser = argparse.ArgumentParser(description=desc, epilog=epil)
parser.error = error_handler
parser.version = vers

""" group arguments  """

group = parser.add_mutually_exclusive_group()

# Increase verbosity
group.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increase output verbosity",
)

""" positional arguments  """

# Save generated password to file
parser.add_argument(
    "-s",
    "--save",
    action="store_true",
    help="Saves the generated password to file in the usrer's home directory. Works with the --name option.",
)

# Delete saved password generated file
parser.add_argument(
    "-d",
    "--delete",
    nargs=1,
    help="Delete the  generated password file. Works with the --save parameter",
)

# Name the saved generated password file. Works with the --save option and defaults to 'generated_password.txt'
parser.add_argument(
    "-n",
    "--name",
    nargs=1,
    help="Name output file. Works with --save option. Ecpects a file name without an extension.",
)

# Run the program
parser.add_argument(
    "-g",
    "--generate",
    dest="generate",
    action="store_true",
    help="Generates a random string",
)

args = parser.parse_args()

if args.verbose:
    verbose = True

if args.save:
    save_to_file = True

if args.name:
    status, data = he(args.name[0])
    if status:
        e_msg_head = cus(255, 100, 100, "Error: ")
        e_msg_body = cus(
            255,
            255,
            255,
            "The name [{}] must not include an extension - e.g. 'file-name.xyz'.".format(
                args.name[0]
            ),
        )
        e_msg = "{} {}".format(e_msg_head, e_msg_body)
        print("{}".format(e_msg))
        exit_prog()
    else:
        name = args.name[0]

if args.generate:
    if verbose:
        msg = cus(230, 255, 230, "... Generating password")
        print("\t\t{}\n".format(msg))

        pwd = gpt()
        pwd_msg = cus(100, 255, 150, "Password Successfully Generated")
        msg = cus(255, 255, 255, pwd)

        print("{}:\t{}".format(pwd_msg, msg))

        if save_to_file:
            if not args.name:
                name = default_name
            if not he(name):
                name += ".txt"
            dest = "{}/{}".format(USER_DIR, name)
            snf(dest, pwd)
            pwd_msg = cus(10, 255, 15, "Password Successfully Saved At {}".format(dest))

            print("{}".format(pwd_msg))

    else:
        pwd = gpt()
        print("{}".format(cus(255, 255, 255, pwd)))

        if save_to_file:
            if not args.name:
                name = default_name
            if not he(name):
                name += ".txt"
            dest = "{}/{}".format(USER_DIR, name)
            snf(dest, pwd)
            pwd_msg = cus(
                100, 255, 150, "Password Successfully Saved At {}".format(dest)
            )

            print("{}".format(pwd_msg))
elif args.delete:
    file_path = args.delete[0]
    if fe(file_path):
        df(file_path)
    else:
        s_msg_header = cus(255, 180, 0, "Info")
        s_msg_body = cus(
            255, 255, 255, "file path: '{}' does not exist".format(file_path)
        )
        s_msg = "{}: {}".format(s_msg_header, s_msg_body)
        print("{}\n".format(s_msg))
exit_prog()
