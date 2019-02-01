import time

from lib.cmd import WhatDirParser
from requesting.request_creator import RequestMaker
from lib.settings import (
    process_file,
    heuristics,
    create_request_headers,
    save_successful_connection,
    BANNER
)
from lib.formatter import (
    info,
    warn,
    error,
    fatal,
    debug
)


def main():
    try:
        full_program_start_time = time.time()
        print(BANNER)
        opts = WhatDirParser().optparse()
        if opts.urlToUse is not None:
            if opts.wordListToUse is not None:
                try:
                    if opts.runVerbose:
                        debug("checking file")
                    open(opts.wordListToUse)
                except:
                    error("wordlist did not open, does it exist?")
                    exit(1)
                if opts.runVerbose:
                    debug("file appears to exist, continuing and testing URL: {}".format(opts.urlToUse))
                test, usable_url = heuristics(opts.urlToUse)
                if not test:
                    fatal(
                        "heuristics have determined that the URL provided is not a valid URL, validate and try again, "
                        "does it have 'http(s)://' in it?"
                    )
                    exit(1)
                if opts.runVerbose:
                    debug("URL passed heuristic vailidation, continuing")
                info("processing your file")
                process_start_time = time.time()
                if opts.runVerbose:
                    debug("file processing start time: {}".format(process_start_time))
                target_data = process_file(opts.wordListToUse)
                process_stop_time = time.time()
                if opts.runVerbose:
                    debug("file process end time: {}".format(process_stop_time))
                info(
                    "file processed in {}(s), total of {} unique string(s) to be used".format(
                        round(process_stop_time - process_start_time), len(target_data)
                    )
                )
                if opts.runVerbose:
                    debug("configuring headers and proxies")
                proxy, headers = create_request_headers(
                    proxy=opts.requestProxy, headers=opts.extraHeaders, user_agent=opts.userAgentRandomize
                )
                if opts.runVerbose:
                    debug("proxy configuration: {}, header configuration: {}, starting attacks".format(proxy, headers))
                results = RequestMaker(
                    usable_url, target_data, threads=opts.amountOfThreads, quiet=opts.runInQuiet,
                    proxy=proxy, headers=headers, save_all=opts.saveAllAttempts, verbose=opts.runVerbose
                ).threaded_response_helper()
                info("a total of {} possible result(s) found".format(len(results)))
                if opts.outputFile is not None:
                    if len(results) != 0:
                        info("saving connections to {}".format(opts.outputFile))
                        save_successful_connection(results, opts.outputFile)
                    else:
                        warn("no results found, skipping file creation", minor=True)
            else:
                warn("must provide a wordlist using the `-w/--words` flag")
                exit(1)
        else:
            warn("must provide a target URL using the `-u/--url` flag")
            exit(1)
        full_program_end_time = time.time()
        info(
            "{} took {}(s) to complete with a total of {} requests".format(
                __name__.split(".")[0], round(full_program_end_time - full_program_start_time),
                len(target_data)
            ))
    except KeyboardInterrupt:
        fatal("user quit")