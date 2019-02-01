import argparse


class StoreDictKeyPairs(argparse.Action):

    """
    custom action to create a dict from a provided string in the format of key=value
    """

    retval = {}

    def __call__(self, parser, namespace, values, option_string=None):
        for kv in values.split(","):
            if ":" in kv:
                splitter = ":"
            else:
                splitter = "="
            if kv.count(splitter) != 1:
                first_equal_index = kv.index(splitter)
                key = kv[:first_equal_index].strip()
                value = kv[first_equal_index + 1:].strip()
                self.retval[key] = value
            else:
                k, v = kv.split(splitter)
                self.retval[k.strip()] = v.strip()
        setattr(namespace, self.dest, self.retval)


class WhatDirParser(argparse.ArgumentParser):

    def __init__(self):
        super(WhatDirParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        mandatory = parser.add_argument_group("mandatory arguments")
        mandatory.add_argument(
            "-u", "--url", dest="urlToUse", default=False, metavar="URL",
            help="Pass a URL to find start directory bruteforcing on (*default=None)"
        )
        mandatory.add_argument(
            "-w", "--words", dest="wordListToUse", default=None, metavar="PATH-TO-WORDLIST",
            help="pass a wordlist to read from, must contain paths one per line (*default=None)"
        )

        request_args = parser.add_argument_group("request arguments")
        request_args.add_argument(
            "-t", "--threads", default=10, dest="amountOfThreads",
            help="Pass an amount of threads to use for the requests (*default=10)",
            type=int
        )
        request_args.add_argument(
            "-H", "--headers", default=None, action=StoreDictKeyPairs, dest="extraHeaders",
            metavar="KEY:VALUE,KEY=VALUE",
            help="pass headers by KEY=VALUE or KEY:VALUE to add them to the requests, to pass multiple use "
                 "key:value1,key:value2,... (*default=None)"
        )
        request_args.add_argument(
            "-p", "--proxy", default=None, dest="requestProxy", metavar="PROTO://PROXY:PORT",
            help="pass a proxy to use during the requests, proto://proxy:port IE socks5://127.0.0.1:9050, "
                 "(*default=None)"
        )
        request_args.add_argument(
            "-a", "--agent", default=False, dest="userAgentRandomize", action="store_true",
            help="pass this flag to grab a random User-Agent and use it, (*default=CUSTOM)"
        )

        misc_args = parser.add_argument_group("misc arguments")
        misc_args.add_argument(
            "-q", "--quiet", action="store_true", default=False,
            help="display only successful connections within status code range, (*default=False)",
            dest="runInQuiet"
        )
        misc_args.add_argument(
            "-o", "--output", metavar="OUTPUT-FILE-PATH", default=None, dest="outputFile",
            help="pass a file name to save all successful connections into a CSV file "
                 "(will append .csv if not present), (*default=None)"
        )
        misc_args.add_argument(
            "--save-all", default=False, action="store_true", dest="saveAllAttempts",
            help="add all attempts as a possible connection even if the status code is not 'good' (*default=False)"
        )
        misc_args.add_argument(
            "--verbose", action="store_true", default=False, dest="runVerbose",
            help="run in verbose mode (more output), (*default=False)"
        )
        return parser.parse_args()
