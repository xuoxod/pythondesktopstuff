import pprint
import json


def pretty_print(data):
    pprint.pprint(data)


def json_print(data):
    pretty = json.dumps(data, indent=4)
    print("{}\n".format(pretty))


def dict_print(data):
    for d in data:
        for key, value in d.items():
            print("{}: {}".format(key, value))
        print("\n")
