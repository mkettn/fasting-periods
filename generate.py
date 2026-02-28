#!/usr/bin/env python3
"""
Usage:
    ./generate.py [options] --ics=FILE --html=FILE

Arguments:
    FILE    output file for switch
    YEAR    set current year to this value

Options:
    --old        set calendar style to old.
    --new        set calendar style to new (the default).
    --year=YEAR  set this year instead of current year.
    --ics=FILE   produce a ics file.
    --html=FILE  produce a html file.
    --lang=LANG  set language, e.g. de_DE
"""
from docopt import docopt
import logging
from datetime import date
import vobject
from FastingCalendar import FastingLevels, getFastingCalendar
from IcsGen import fastdays2ics
from HtmlGen import fastdays2html
from locale import setlocale, LC_ALL

ARGV = docopt(__doc__)
current_year = date.today().year
if ARGV["--year"]:
    try:
        current_year = int(ARGV["--year"])
    except ValueError:
        logging.warning(f"value '{i}' for year not recognized")

if ARGV["--lang"]:
    try:
        setlocale(LC_ALL, ARGV["--lang"]+".UTF-8")
    except Exception as e:
        logging.warning(str(e))

fasting_days = getFastingCalendar(current_year, ARGV["--old"])

# german texts:
fl2txtde={
    FastingLevels.NO_FASTING: "kein Fasten",
    FastingLevels.NO_MEAT: "kein Fleisch",
    FastingLevels.NO_DAIRY: "keine Milchprodukte, Eier",
    FastingLevels.NO_FISH: "kein Fisch",
    FastingLevels.NO_OIL: "kein Öl"
}

fastdays2ics(fasting_days, fl2txtde, ARGV["--ics"])
title = f"Fasting calendar {current_year}"
fastdays2html(current_year, fasting_days, fl2txtde, ARGV["--html"], title, f"<h1>{title}</h1>")