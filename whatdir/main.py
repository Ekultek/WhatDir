import time

from lib.cmd import WhatDirParser
from requesting.request_creator import RequestMaker
from lib.settings import (
    process_file,
    heuristics,
    create_request_headers,
    BANNER
)
from lib.formatter import (
    info,
    warn,
    error,
    fatal
)


def main():
    try:
        print(BANNER)
        opts = WhatDirParser().optparse()
        if opts.urlToUse is not None:
            if opts.wordListToUse is not None:
                try:
                    open(opts.wordListToUse)
                except:
                    error("wordlist did not open, does it exist?")
                    exit(1)
                test, usable_url = heuristics(opts.urlToUse)
                if not test:
                    fatal(
                        "heuristics have determined that the URL provided is not a URL, validate and try again, "
                        "does it have 'http(s)://' in it?"
                    )
                    exit(1)

                info("processing your file")
                process_start_time = time.time()
                target_data = process_file(opts.wordListToUse)
                process_stop_time = time.time()
                info(
                    "file processed in {}(s), total of {} unique string(s) to be used".format(
                        round(process_stop_time - process_start_time), len(target_data)
                    )
                )
                proxy, headers = create_request_headers(
                    proxy=opts.requestProxy, headers=opts.extraHeaders, user_agent=opts.userAgentRandomize
                )
                results = RequestMaker(
                    usable_url, target_data, threads=opts.amountOfThreads, quiet=opts.runInQuiet,
                    proxy=proxy, headers=headers
                ).threaded_response_helper()
                info("a total of {} possible results found".format(len(results)))
            else:
                warn("must provide a wordlist using the `-w/--words` flag")
                exit(1)
        else:
            warn("must provide a target URL using the `-u/--url` flag")
            exit(1)
    except KeyboardInterrupt:
        fatal("user quit")