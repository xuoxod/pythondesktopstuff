#! /usr/bin/python3

import argparse
from multiprocessing.dummy import current_process
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PlatformConstants import USER_DIR as udir, LINE_SEP as lsep
from custom_modules.PatternConstants import has_ext
from custom_modules.PasswordGenerator import generate_password_thread as gpt
from custom_modules.FileOperator import save_new_file as snf, delete_file
from custom_modules.FileValidator import (
    file_exists,
    is_dir,
    is_file,
)

cus = cms["custom"]
msg = None
desc = "This program can perform various operations on files, including directories."
epil = "This program runs with root level privilege."
vers = "%prog 0.1"
pwd = ""
default_name = "generated-password.txt"
verbose = False
save_to_file = False


msg_level_switch = {
    "info": lambda m: cus(255, 255, 255, m),
    "error": lambda m: cus(255, 77, 77, m),
    "warn": lambda m: cus(255, 200, 0, m),
    "succ": lambda m: cus(100, 255, 0, m),
}


def exit_prog(exit_code=0):
    sys.exit(exit_code)


def error_handler(*args):
    cus = cms["custom"]
    e_msg_header = cus(255, 120, 120, "Error:")
    e_msg_body = cus(255, 255, 255, "{}".format(args[0]))
    e_msg = "\n\t{} {}\n".format(e_msg_header, e_msg_body)
    print("{}".format(e_msg))
    exit_prog()


def create_msg(msg):
    cus = cms["custom"]
    if len(msg) > 0:
        return "{}".format(cus(255, 255, 255, msg))


def config_msg(msg, level="info"):
    try:
        method = msg_level_switch[level]
        return method(msg)
    except KeyError as ke:
        print("{} is not available".format(level))


def print_msg(msg):
    print("{}".format(msg))


parser = argparse.ArgumentParser(description=desc, epilog=epil)
parser.error = error_handler
parser.version = vers


""" positional arguments  """

# Delete file or directory
parser.add_argument(
    "-d",
    "--delete",
    nargs=1,
    help="Delete given file path.",
)

# Set a warning flag
parser.add_argument(
    "-w", "--warn", action="store_true", help="Notify user whether file or directory."
)

# Set confirmation flag
parser.add_argument(
    "-c", "--confirm", action="store_true", help="Requests user to confirm action."
)

parser.add_argument("-t", "--test", nargs=2, help="Test config_msg method")

args = parser.parse_args()

if args.delete:
    file_path = args.delete[0]

    if file_exists(file_path):
        if args.warn:
            if is_file(file_path):
                msg = "{} is a file".format(file_path)
            elif is_dir(file_path):
                msg = "{} is a directory".format(file_path)
            print_msg(create_msg(msg))

        if args.confirm:
            msg_to_user = create_msg(
                "You are about to delete {}. Continue Y/n?".format(file_path)
            )
            user_input = input("{}\t".format(msg_to_user))

            if user_input.strip() == "y" or user_input.strip() == "Y":
                msg = "Deleting {}".format(file_path)
                print_msg(create_msg(msg))
        else:
            msg = "Deleting {}".format(file_path)
            print_msg(create_msg(msg))
    else:
        s_msg_header = cus(255, 180, 0, "Info")
        s_msg_body = cus(
            255, 255, 255, "file path: '{}' does not exist".format(file_path)
        )
        s_msg = "{}: {}".format(s_msg_header, s_msg_body)
        print("{}\n".format(s_msg))

elif args.test:
    arg = args.test[0]
    lev = args.test[1]
    msg = config_msg(arg, lev)
    print_msg(msg)
