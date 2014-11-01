## Kimsufi availability

Kimsufi servers are very interesting but extremely difficult to obtain. This script parses the OVH API and sends you a mail when a server is available.

## Usage

    Usage:
      kimsufi.py [options]
      kimsufi.py <model>... [options]

    Options:
      -h, --help     Show this help.
      -v, --version  Show version.
      -m, --mail     Send a mail when a server is available.

    Examples:
      kimsufi.py
      kimsufi.py KS-1 KS-3
      kimsufi.py KS-1 --mail


## Installation

The script works on Python 2.x and 3.x. It's just a simple script, so no _setup.py_ is offer :

    git clone https://github.com/ncrocfer/kimsufi-availability.git
    cd kimsufi-availability
    python kimsufi.py

## Using Cron

You can create a cron job to send you a mail periodically. For example :

    * * * * * python kimsufi.py KS-1 --mail

## License

This script is under the [Beerware](http://en.wikipedia.org/wiki/Beerware) license.
