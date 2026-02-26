#!/usr/bin/env python3
"""
Usage:
    ./generate.py [options] --ics=FILE --html=FILE

Arguments:
    FILE    output file for switch
    YEAR    set current year to this value

Options:
    --old        set calendar style to old.
    --year=YEAR  set this year instead of current year.
    --ics=FILE   produce a ics file.
    --html=FILE  produce a html file.
"""
from docopt import docopt
import logging
from enum import Enum
from datetime import date
from icalendar import Calendar, Event
from FastingCalendar import FastingLevels, getFastingCalendar

# german texts:
fl2txtde={
    FastingLevels.NO_FASTING: "kein Fasten",
    FastingLevels.NO_MEAT: "kein Fleisch",
    FastingLevels.NO_DAIRY: "keine Milchprodukte, Eier",
    FastingLevels.NO_FISH: "kein Fisch",
    FastingLevels.NO_OIL: "kein Öl"
}


ARGV = docopt(__doc__)
current_year = date.today().year
if ARGV["--year"]:
    try:
        current_year = int(ARGV["--year"])
    except ValueError:
        logging.WARN(f"value '{i}' for year not recognized")

fasting_days = getFastingCalendar(current_year, ARGV["--old"])

events = []

for k,v in fasting_days.items():
    if v==FastingLevels.NO_FASTING:
        continue
    events.append(Event.new(summary=fl2txtde[v], start=k))
    
with open(ARGV["--ics"], 'w') as f:
    icsCal = Calendar(subcomponents=events)

    f.writelines(icsCal.to_ical())