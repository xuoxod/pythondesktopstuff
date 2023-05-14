#! /usr/bin/python3
import pymongo, sys, os
from custom_modules.Utils import clear_screen as cls
from custom_modules.ConsoleMessenger import CONSOLE_MESSENGER_SWITCH as cms
from custom_modules.PlatformConstants import LINE_SEP as lsep
from custom_modules.DataPrinter import (
    pretty_print as pp,
    json_print as jp,
    dict_print as dp,
)
from custom_modules.PatternConstants import (
    is_single_number_only as isno,
    is_single_alpha_only as isao,
    is_number_only as ino,
    is_alpha_only as iao,
)

db_client = pymongo.MongoClient(
    "mongodb+srv://rmtadmin:Ic03BmGAUSbbWwKL@cluster0.mrx2r.mongodb.net/rmtusers?retryWrites=true&w=majority"
)

cus = cms["custom"]
user_input = ""
server_info = db_client.server_info
databases = db_client.list_database_names()
database = None
database_name = None
db = None
collections = None
collection = None
collection_name = None
answer = None


def exit_prog(exit_code=0):
    cls()
    sys.exit(exit_code)


def graceful_exit(exit_code=0):
    sys.exit(exit_code)


def handle_post_collection_query():
    global user_input
    global answer
    global collection_name

    user_input = None
    answer = None

    user_input = input(
        "\n1. Continue using collection {}\n2. Choose a different collection\n3. Choose a different database\n0. Exit program\n".format(
            collection_name.upper()
        )
    )

    answer = user_input.strip()

    if ino(answer) and isno(answer):
        if answer == "1":
            send_query_to_collection()
        elif answer == "2":
            handle_collection_input()
        elif answer == "3":
            handle_database_input()
        elif answer == "0":
            exit_prog()
        else:
            handle_post_collection_query()


def handle_custom_query():
    global database_name
    global collection_name
    global user_input
    global database

    collection = database[collection_name]

    user_input = input(
        "\nEnter one or more comma separated queries e.g. field=value, field={key:value}\n"
    )

    raw_query = user_input.strip()
    results = None
    query = {}

    if "," in raw_query:
        comma_split = raw_query.split(",")

        for c in comma_split:
            equals_split = c.split("=")

            query["{}".format(equals_split[0])] = equals_split[1]
    else:
        equals_split = raw_query.split("=")

        query["{}".format(equals_split[0])] = equals_split[1]

    try:
        results = collection.find(query)
    except Exception as e:
        print("\n{}\n".format(e))

    print(
        "\nDatabase: {}\nCollection: {}\nQuery: {}\n".format(
            database_name.upper(), collection_name.upper(), query
        )
    )

    print("\nResults:\t{}\n".format(results))

    for x in results:
        print("{}\n".format(x))

    try:
        jp(results)
    except TypeError as te:
        dp(results)

    handle_post_collection_query()


def send_query_to_collection():
    global collection_name
    collection = database[collection_name]
    os.system("clear")
    user_input = input(
        "\nQuery Options\n\t1. Find One\n\t2. Find All\n\t3. Find all, return one or more fields\n\t4. Enter valid custom query\n"
    )
    answer = user_input.strip()

    if ino(answer) and isno(answer):
        if answer == "1":
            query = collection.find_one()
            os.system("clear")
            print(
                "Database: {}\nCollection: {}\nQuery: Find One\n".format(
                    database_name.upper(), collection_name.upper()
                )
            )
            try:
                jp(query)
            except TypeError as te:
                pp(query)
            handle_post_collection_query()
        elif answer == "2":
            query = collection.find()
            os.system("clear")
            print(
                "Database: {}\nCollection: {}\nQuery: Find All\n".format(
                    database_name.upper(), collection_name.upper()
                )
            )
            try:
                jp(query)
            except TypeError as te:
                dp(query)
            handle_post_collection_query()
        elif answer == "3":
            os.system("clear")
            fields = input(
                "\nEnter one or more fields to return. Multiple fields must be comma separated.\t"
            )

            if fields:
                obj_field = {}

                if "," in fields.strip():
                    field_comma_split = fields.split(",")

                    if len(field_comma_split) > 0:
                        for f in field_comma_split:
                            obj_field["{}".format(f.strip())] = 1

                        query = collection.find({}, obj_field)
                        try:
                            jp(query)
                        except TypeError as te:
                            dp(query)
                else:
                    obj_field["{}".format(fields.strip())] = 1

                    query = collection.find({}, obj_field)
                    try:
                        jp(query)
                    except TypeError as te:
                        dp(query)

            handle_post_collection_query()
        elif answer == "4":
            handle_custom_query()
        else:
            m_header = cus(250, 100, 130, "Choice Error:")
            m_body = cus(
                240,
                240,
                200,
                "{} is not a valid database choice".format(user_input),
            )
            msg = "\n{}\t{}".format(m_header, m_body)
            print("{}\n".format(msg))
            user_input = None
            send_query_to_collection()
    else:
        m_header = cus(250, 100, 130, "Choice Error:")
        m_body = cus(
            240,
            240,
            200,
            "{} is not a valid query choice".format(user_input),
        )
        msg = "\n{}\t{}".format(m_header, m_body)
        print("{}\n".format(msg))
        user_input = None
        os.system("sleep 5")
        send_query_to_collection()


def handle_database_answer():
    global answer
    global user_input
    os.system("clear")

    answer = user_input.strip()

    if ino(answer) and isno(answer):
        if answer == "1":
            handle_collection_input()
        elif answer == "2":
            user_input = None
            return
        elif answer == "0":
            exit_prog()
        else:
            m_header = cus(250, 100, 130, "Choice Error:")
            m_body = cus(
                240,
                240,
                200,
                "{} is not a valid answer".format(user_input),
            )
            msg = "\n{}\t{}".format(m_header, m_body)

            print("{}\n".format(msg))

            user_input = input(
                "1. Continue with {} database\n2. Choose another database\n0. Quit program\n".format(
                    database_name.upper()
                )
            )

            handle_database_answer()

    else:
        m_header = cus(250, 100, 130, "Choice Error:")
        m_body = cus(
            240,
            240,
            200,
            "{} is not a valid answer".format(user_input),
        )
        msg = "\n{}\t{}".format(m_header, m_body)

        print("{}\n".format(msg))

        user_input = input(
            "1. Continue with {} database\n2. Choose another database\n0. Quit program\n".format(
                database_name.upper()
            )
        )
        handle_database_answer()


def handle_collection_input():
    global database
    global database_name
    global collection_name
    global user_input
    os.system("clear")

    collection_names = database.list_collection_names()
    cols = ""

    if len(collection_names) > 0:
        for i, c in enumerate(collection_names, start=1):
            if i < len(collection_names):
                cols += "\t{}. {}\n".format(i, c)
            else:
                cols += "\t{}. {}".format(i, c)

        user_input = input(
            "\nChoose a collection by number\n{}\n0. Quit program\n".format(cols)
        )

        is_number, number = ino(user_input)

        if is_number:
            if isno(number.string):
                try:
                    collection_name = collection_names[int(number.string) - 1]
                    print(
                        "\nYou chose the {} collection.\n".format(
                            collection_name.upper()
                        )
                    )

                    user_input = input(
                        "\n1. Continue with {}\n2. Choose a different collection\n3. Choose a different database\n0. Quit program\n".format(
                            collection_name
                        )
                    )

                    if user_input.strip() == "0":
                        exit_prog()
                    elif user_input.strip() == "1":
                        send_query_to_collection()
                    elif user_input.strip() == "2":
                        handle_collection_input()
                    elif user_input.strip() == "3":
                        user_input = None
                        handle_database_input()
                    else:
                        handle_collection_input()

                except IndexError as ie:
                    m_header = cus(250, 100, 130, "Choice Error:")
                    m_body = cus(
                        240,
                        240,
                        200,
                        "{} is not a valid collection choice".format(number.string),
                    )
                    msg = "\n{}\t{}".format(m_header, m_body)

                    print("{}\n".format(msg))
                    handle_collection_input()
            else:
                m_header = cus(250, 100, 130, "Choice Error:")
                m_body = cus(
                    240,
                    240,
                    200,
                    "{} is not a valid collection choice".format(number.string),
                )
                msg = "\n{}\t{}".format(m_header, m_body)

                print("{}\n".format(msg))
                handle_collection_input()

        else:
            m_header = cus(250, 100, 130, "Choice Error:")
            m_body = cus(
                240,
                240,
                200,
                "{} is not a valid collection choice".format(user_input),
            )
            msg = "\n{}\t{}".format(m_header, m_body)

            print("{}\n".format(msg))
            handle_collection_input()

    else:
        msg = cus(
            230,
            200,
            210,
            "database {} has no collections".format(database_name.upper()),
        )
        print("{}\n".format(msg))
        return


def handle_database_input():
    global user_input
    global databases
    global database
    global database_name
    global collections
    global collection
    global answer

    if user_input:
        is_number, number = ino(user_input)

        if is_number:
            try:
                database_name = databases[int(number.string) - 1]
                database = db_client[database_name]

                print("\nYou chose the {} database.\n".format(database_name.upper()))

                user_input = input(
                    "1. Continue with {} database\n2. Choose another database\n0. Quit program\n".format(
                        database_name.upper()
                    )
                )

                handle_database_answer()

            except IndexError as ie:
                m_header = cus(250, 100, 130, "Choice Error:")
                m_body = cus(
                    240,
                    240,
                    200,
                    "{} is not a valid database choice".format(number.string),
                )
                msg = "\n{}\t{}".format(m_header, m_body)

                print("{}\n".format(msg))
                return

        else:
            m_header = cus(250, 100, 130, "Choice Error:")
            m_body = cus(
                240, 240, 200, "{} is not a valid database choice".format(user_input)
            )
            msg = "\n{}\t{}".format(m_header, m_body)

            print("{}\n".format(msg))
            return


def run():
    global user_input
    dbs = ""

    for i, d in enumerate(databases, start=1):
        if i < len(databases):
            dbs += "\t{}. {}\n".format(i, d)
        else:
            dbs += "\t{}. {}".format(i, d)

    try:
        while (
            user_input != "x"
            and user_input != "q"
            and user_input != "exit"
            and user_input != "quit"
        ):
            user_input = input(
                "\nChoose database by number\n{}\nQuit program\n\texit (x)\n\tquit (q)\n".format(
                    dbs
                )
            )

            if user_input and not (
                user_input == "x"
                or user_input == "q"
                or user_input == "exit"
                or user_input == "quit"
                or user_input == "0"
            ):
                handle_database_input()
    except KeyboardInterrupt as ki:
        graceful_exit()
    exit_prog()


run()
