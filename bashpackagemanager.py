#! /usr/bin/python3
import os
import sys
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PlatformConstants import LINE_SEP as lsep
from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc
from data.packages import bash_packs as pkgs

cus = cms["custom"]


def exit_prog():
    sys.exit(0)


def start_upgrade():
    msg = cus(255, 255, 255, "Upgrading the following packages:")
    print("\t\t{}".format(msg))
    print(*pkgs, sep="\n")
    print("{}{}".format(lsep, lsep))


def start_installation():
    msg = cus(255, 255, 255, "Installing the following packages:")
    print("\t\t{}".format(msg))
    print(*pkgs, sep="\n")
    print("{}{}".format(lsep, lsep))


def _upgrade():
    for p in pkgs:
        result = os.system("sudo apt upgrade {} -y".format(p))
        print("Results: {}".format(result))

        if result == 0:
            msg = cus(55, 244, 55, "Upgraded package: {}".format(p))
            print("{}{}".format(msg, lsep))
            continue
        else:
            msg = cus(244, 55, 55, "Could not upgrade package:")
            print("{}{}".format(msg, lsep))
            continue


def _install():
    for p in pkgs:
        result = os.system("sudo apt install {} -y".format(p))
        print("Results: {}".format(result))

        if result == 0:
            msg = cus(55, 244, 55, "Installed package: {}".format(p))
            print("{}{}".format(msg, lsep))
            continue
        else:
            msg = cus(244, 55, 55, "Could not upgrade package:")
            print("{}{}".format(msg, lsep))
            continue


def upgrade():
    start_upgrade()
    _upgrade()


def install():
    start_installation()
    _install()


ACTION = {"install": install, "upgrade": upgrade}

if argsc == 1:
    try:
        arg = args[0]
        action = ACTION[arg]
        action()
    except KeyError as ke:
        msg_head = cus(244, 100, 100, "{} is not a valid argument".format(ke))
        msg_body = cus(244, 244, 244, "Could not find key [{}]".format(arg))
        msg = "{}:\t{}".format(msg_head, msg_body)
        print("{}{}".format(msg, lsep))
    finally:
        exit_prog()
else:
    print("Expected one argument but received {}".format(argsc))
    print(*args, sep="\n")
    exit_prog()
