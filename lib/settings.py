import re
import sys
import platform
try:
    from urlparse import urlparse
except Exception:
    from urllib.parse import urlparse


# this is a regex to validate a URL. It was taken from Django's URL validation technique
# reference can be found here:
# `https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778#7160778`
URL_VALIDATION = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

# version number
VERSION = "0.1"

# version type, either dev or stable
VERSION_TYPE = "dev" if VERSION.count(".") > 1 else "stable"

# sexy banner to make it all come together
BANNER = """\033[98m
.-.   .-..-.          .-. .---.  _      
: :.-.: :: :         .' `.: .  ::_;     
: :: :: :: `-.  .--. `. .': :: :.-..--. 
: `' `' ;: .. :' .; ; : : : :; :: :: ..'
 `.,`.,' :_;:_;`.__,_;:_; :___.':_;:_;\033[0m
\033[96m/version/{}/{}\033[0m\n 
""".format(VERSION_TYPE, VERSION)

DEFAULT_USER_AGENT = "whatdir/{} (Language={}; Platform={})".format(
    VERSION, sys.version.split(" ")[0], platform.platform().split("-")[0]
)


def heuristics(url):
    """
    basic heuristic check to see if the URL is validated or not
    """
    if not URL_VALIDATION.match(url):
        return False, None
    parsed_url = urlparse(url)
    usable_url = "{}://{}".format(parsed_url.scheme, parsed_url.netloc)
    return True, usable_url


def process_file(filename, chunk=1024):
    """
    process a file in chunks, this should save some time when processing large files
    testing with 37 million lines the file processed in just under 40 seconds
    """
    retval = set()
    with open(filename) as data:
        while True:
            piece = data.read(chunk)
            if piece:
                for item in piece.splitlines():
                    if not str(item).startswith("/"):
                        item = "/{}".format(item.strip())
                    retval.add(item.strip())
            else:
                break
    return retval


def grab_random_user_agent():
    """
    grab a random user agent out of a file
    """
    import os
    import random

    path = "{}/etc/user_agents.txt".format(os.getcwd())
    with open(path) as agents:
        return random.choice(agents.readlines()).strip()


def create_request_headers(proxy=None, headers=None, user_agent=False):
    """
    configure the request headers and proxy information
    """
    if proxy is not None:
        proxy_retval = {"http": proxy, "https": proxy}
    else:
        proxy_retval = {}
    if headers is not None:
        header_retval = {}
        for k in headers.keys():
            header_retval[k] = headers[k]
    else:
        header_retval = {"Connection": "close"}
    if user_agent:
        header_retval["User-Agent"] = grab_random_user_agent()
    else:
        header_retval["User-Agent"] = DEFAULT_USER_AGENT
    return proxy_retval, header_retval

