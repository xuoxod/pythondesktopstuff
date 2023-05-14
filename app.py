#! /usr/bin/python3
import re, sys, time
from custom_modules.Utils import clear_screen as cls
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PlatformConstants import LINE_SEP as lsep
from custom_modules.PatternConstants import (
    is_number_only as isnumber,
    is_alpha_only as isletter,
)
from custom_modules.ArgumentManager import filtered as args, filtered_count as argsc


cus = cms["custom"]
user_input = ""


def exit_prog(exit_code=0):
    cls()
    sys.exit(exit_code)


# @param  word: String - the string to search
# @param  search: String - the string to search for
# @return Boolean - returns True if list contains at least one match
def contains(word, search):
    matches = re.findall(word, search)
    return len(matches) > 0


# @param  word: String - the string to search
# @return Boolean - returns True if list contains at least one match
# @return Object - findall results
def contains_nonalpha(word):
    nonalpha = re.compile(r"[0-9\,\.\\\/\!\?\;\:\"\']+")
    matches = re.search(nonalpha, word)
    return matches != None, matches.span()


def handle_input():
    users_input_space_split = user_input.split(" ")

    m_header = cus(250, 222, 0, "You Entered:")
    m_body = cus(250, 250, 250, "{}".format(user_input))
    msg = "{} {}{}".format(m_header, m_body, lsep)

    print("Word Count:\t{}".format(len(users_input_space_split)))
    print("{}".format(msg))


def debug_input():
    captured_user_input = user_input
    match, matches = contains_nonalpha(str(captured_user_input))

    if match:
        m_header = cus(240, 230, 20, "Found Non-alpha characters")
        msg = "{}".format(m_header)
        print("{}\n".format(msg))
        print("{}".format(matches))
    else:
        m_header = cus(240, 230, 20, "You entered:")
        m_body = cus(200, 230, 20, "{}".format(captured_user_input))
        msg = "{} {}".format(m_header, m_body)
        print("{}\n".format(msg))


def run():
    global user_input
    try:
        while (
            user_input != "x"
            and user_input != "q"
            and user_input != "exit"
            and user_input != "quit"
        ):
            user_input = input(
                "Enter something:\tType exit (x) or quit (q) to end program\n\t"
            )

            if user_input and not (
                user_input == "x"
                or user_input == "q"
                or user_input == "exit"
                or user_input == "quit"
            ):
                handle_input()
                debug_input()
    except KeyboardInterrupt as ki:
        exit_prog()
    exit_prog()


run()
