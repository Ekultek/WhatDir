import threading
try:
    import queue
except ImportError:
    import Queue as queue

import requests

from lib.formatter import info


class RequestMaker(object):

    response_retval = []

    def __init__(self, url, targets, **kwargs):
        self.url = url
        self.targets = targets
        self.proxy = kwargs.get("proxy", {})
        self.headers = kwargs.get("headers", {})
        self.good_status_codes = (200, 301, 403)
        self.threads = kwargs.get("threads", 10)
        self.queue = queue.Queue()
        self.quiet = kwargs.get("quiet", False)

    def threader(self):
        while True:
            target = self.queue.get()
            self.threaded_get_response(target)
            self.queue.task_done()

    def threaded_get_response(self, target):
        try:
            req = requests.get(target, proxies=self.proxy)
            if req.status_code in self.good_status_codes:
                directory_retval = target.split("/")[-1]
                status_code = req.status_code
                print("/{} ({})".format(directory_retval, status_code))
                self.response_retval.append((target, req.status_code))
            else:
                if not self.quiet:
                    directory_retval = target.split("/")[-1]
                    status_code = req.status_code
                    print("/{} ({})".format(directory_retval, status_code))
                self.response_retval.append((target, req.status_code))
        except Exception:
            pass
        except KeyboardInterrupt:
            self.queue.all_tasks_done()

    def threaded_response_helper(self):
        info("queuing everything")
        for target in self.targets:
            self.queue.put("{}{}".format(self.url, target))
        info("starting directory bruteforcing with {} thread(s)".format(self.threads))
        try:
            for _ in range(self.threads):
                t = threading.Thread(target=self.threader)
                t.daemon = True
                t.start()
            self.queue.join()
        except (KeyboardInterrupt, SystemExit):
            self.queue.all_tasks_done()
        return self.response_retval




