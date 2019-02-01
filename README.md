# WhatDir

WhatDir is another addition to the `What` series. The main objective of WhatDir is to bruteforce web application directories using a provided wordlist. Some features of WhatDir:

 - Ability to pass a proxy
 - Ability to pass your own headers
 - Ability to use User-Agent randomization or use the default custom User-Agent
 - Multi-threaded with a default of 10 threads
 - Quick file processing, on average it can process 37 million lines in under 40 seconds

# Usage

The list of arguments is simple, and here's a list of them:

```bash
usage: whatdir.py [-h] [-u URL] [-w PATH-TO-WORDLIST] [-t AMOUNTOFTHREADS]
                  [-H KEY:VALUE,KEY=VALUE] [-p PROTO://PROXY:PORT] [-a] [-q]

optional arguments:
  -h, --help            show this help message and exit

mandatory arguments:
  -u URL, --url URL     Pass a URL to find directories
  -w PATH-TO-WORDLIST, --words PATH-TO-WORDLIST
                        pass a wordlist to use

request arguments:
  -t AMOUNTOFTHREADS, --threads AMOUNTOFTHREADS
                        Pass an amount of threads
  -H KEY:VALUE,KEY=VALUE, --headers KEY:VALUE,KEY=VALUE
                        pass headers by KEY=VALUE or KEY:VALUE to add them to
                        the requests, to pass multiple use
                        key:value1,key:value2,...
  -p PROTO://PROXY:PORT, --proxy PROTO://PROXY:PORT
                        pass a proxy to use during the requests,
                        proto://proxy:port IE socks5://127.0.0.1:9050
  -a, --agent           pass this flag to grab a random User-Agent and use it

misc arguments:
  -q, --quiet           display only successful connections
```

# Installation

The installation is simple all you have to do is run:

```bash
pip install -r requirements.txt
```

and then run:

```bash
python whatdir.py -h
```

This should install everything you need and you should be good to go.

# Bugs

If you manage to find a bug or an improvement, please create an issue [here](https://github.com/Ekultek/WhatDir/issues)

# Side note

WhatDir is still in a very new stage and I'm really only releasing it to figure out what improvements should be made, the end goal is to have a very quick lightweight directory bruteforcer that will be able to be ported quickly and efficiently