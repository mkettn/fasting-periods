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
    --lang=FILE  get translation from file.
"""
from docopt import docopt
import yaml
import logging
from datetime import date
import vobject
from FastingCalendar import FastingLevels, getFastingCalendar
from IcsGen import fastdays2ics
from HtmlGen import fastdays2html, get_legend
from locale import setlocale, LC_ALL
from os.path import dirname,isfile

ARGV = docopt(__doc__)
current_year = date.today().year
if ARGV["--year"]:
    try:
        current_year = int(ARGV["--year"])
    except ValueError:
        logging.warning(f"value '{i}' for year not recognized")

tf = dirname(__file__)+"/translations/en.yml"

if ARGV["--lang"]:
    ltf = dirname(__file__)+"/translations/"+ARGV["--lang"]+".yml"
    if isfile(ARGV["--lang"]):
        tf = ARGV["--lang"]
    elif isfile(ltf):
        tf = ltf

transl = {}
with open(tf, 'r') as fd:
    transl = yaml.safe_load(fd)

cal_style = transl["style"][1]

if ARGV["--old"]:
    cal_style = transl["style"][0]

fasting_days = getFastingCalendar(current_year, ARGV["--old"])

fastdays2ics(fasting_days, transl["levels"], ARGV["--ics"])
title = transl["title"] + f" {current_year} {cal_style}"
fastdays2html(current_year, fasting_days, transl, ARGV["--html"], title, f'<h1 class="noprint">{title}</h1>', get_legend(transl["levels"]))