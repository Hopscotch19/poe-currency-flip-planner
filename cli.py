import argparse
import itertools
from src.pathfinder import PathFinder
from src.constants import currencies
from src.backends import poeofficial
from src.backends import poetrade


def log_conversions(conversions, currency, limit):
    for c in conversions[currency][:limit]:
        log_conversion(c)


def log_conversion(c):
    print("{} {} -> {} {}: {} {}".format(c['starting'],
                                         c['from'], c['ending'], c['to'], c['winnings'], c['to']))
    for t in c['transactions']:
        print("\t@{} Hi, I'd like to buy your {} {} for {} {}. ({})".format(
            t['contact_ign'], t['received'], t['to'], t['paid'], t['from'], t['conversion_rate']))
    print("\n")


parser = argparse.ArgumentParser(description="CLI interface for PathFinder")
parser.add_argument("--league", default="Delve",
                    help="League specifier, ie. 'Delve', 'Hardcore Delve' or 'Flashback Event (BRE001)'. Defaults to 'Delve'.")
parser.add_argument("--currency", default="all",
                    help="Full name of currency to flip, ie. 'Cartographer\'s Chisel, or 'Chaos Orb'. See a full list of currency names under src/constants.py. Defaults to all currencies.")
parser.add_argument("--limit", default=3,
                    help="Limit the number of displayed conversions. Defaults to 3.")
parser.add_argument("--poetrade", default=False,
                    help="Flag to fetch trading data from poe.trade instead of pathofexile.com/trade.")
arguments = parser.parse_args()

league = arguments.league
currency = arguments.currency
limit = arguments.limit
use_poetrade = arguments.poetrade

backend = poetrade if use_poetrade else poeofficial

chosen_currencies = dict(itertools.islice(currencies.items(), 0, 15))
p = PathFinder(league, chosen_currencies, backend)
p.run(3, True)
try:
    if currency is "all":
        for c in chosen_currencies:
            log_conversions(p.results, c, limit)
    else:
        log_conversions(p.results, currency, limit)
except KeyError:
    print("Could not find any proftiable conversions for {} in {}".format(
        currency, league))
