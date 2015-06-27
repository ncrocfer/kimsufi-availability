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

## Output example

    $ python kimsufi.py KS-1

    KS-1
    ====
    Gravelines : 1H-high
    Strasbourg : unavailable
    Roubaix : unavailable
    Beauharnois : unavailable

    =======
    RESULT : 1 server is available on Kimsufi
    =======

## Installation

The script works on Python 2.x and 3.x. It's just a simple script, so no _setup.py_ is offer :

    $ git clone https://github.com/ncrocfer/kimsufi-availability.git
    $ cd kimsufi-availability
    $ pip install -r requirements.txt
    $ python kimsufi.py

## Mail configuration

A mail can be sent with the `--mail` option. You can configure it with a `config.json` file : 

    $ cp config.json.sample config.json
    $ vim config.json
    {
        "email": {
                "host": "...",
                "port": 587,
                "username": "...",
                "password": "...",
                "mail_from": "...",
                "mail_to": "..."
        }
    }

## Using Cron

You can create a cron job to send you a mail periodically. For example :

    * * * * * python kimsufi.py KS-1 --mail

## License

This script is under the [Beerware](http://en.wikipedia.org/wiki/Beerware) license.
