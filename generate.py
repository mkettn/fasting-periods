#!/usr/bin/env python3
"""
Usage:
    ./generate.py [options] --ics=FILE --html=FILE

Arguments:
    FILE    output file for switch
    YEAR    set current year to this value

Options:
    --cal=STYLE  set calendar style (old or new). [default: old]
    --year=YEAR  set this year instead of current year.
    --ics=FILE   produce a ics file.
    --html=FILE  produce a html file.
"""
from docopt import docopt
import logging
from enum import Enum
import datetime
from datetime import timedelta, date
from dateutil.easter import easter, EASTER_ORTHODOX

class FastingLevels(Enum):
    NO_FASTING=0 # everything allowed
    NO_MEAT=1 # no meat, diary, eggs, fish allowed
    NO_DAIRY=2 # all of the previous except diary and eggs
    NO_FISH=3 # all of the previous except fish
    NO_OIL=4 # all of the previous except oils

# timedelta for one day
TD_ONE_DAY = timedelta(days=1)

def mark_range(fc:map, start:datetime.date,days:int, lvl:FastingLevels):
    """ mark range in fasting calendar"""
    cd = start
    for _ in range(days):
        fc[start] = lvl
        cd+=TD_ONE_DAY


ARGV = docopt(__doc__)
# FIXME(mke): calculate offset to gregorian calendar day
ORTHODOX_OFFSET_DAYS = 13
current_year = date.today().year
if ARGV["--year"]:
    try:
        current_year = int(ARGV["--year"])
    except ValueError:
        logging.WARN(f"value '{i}' for year not recognized")

first_day_of_year = date(current_year, 1,1)
last_day_of_year = date(current_year, 12,31)

style = ARGV["--cal"]
offset = timedelta()
if style == "old":
    offset = timedelta(days=ORTHODOX_OFFSET_DAYS)
elif style == "new":
    pass
else:
    logging.WARN(f"unknown calendar style: '{style}'")
    exit(1)

## fixed feast days:
christmas = date(current_year, 12, 25)+offset
theophany = date(current_year, 1, 6)+offset
annunciation_of_the_theotokos = date(current_year, 3, 25)+offset
dormition_of_the_theotokos = date(current_year, 8, 15)+offset
nativity_of_the_theotokos = date(current_year, 9, 8)+offset
feast_of_st_peter_paul = date(current_year, 6, 29)+offset

# moving feast days:
easter_sunday = easter(current_year, EASTER_ORTHODOX)
ascension_of_christ = easter_sunday+timedelta(days=40)
pentecost = easter_sunday+timedelta(days=50)

# map for all days of current year -> FastingLevels:
fasting_days = {}
curr_day = first_day_of_year

# assign all weekdays:
while curr_day < last_day_of_year:
    if curr_day.weekday() in [2,4]:
        fasting_days[curr_day] = FastingLevels.NO_OIL
    curr_day+=TD_ONE_DAY


#### EASTER ####
### week of lost son
curr_day = easter_sunday-timedelta(weeks=10)+TD_ONE_DAY # mon
# whole week to fasting
mark_range(fasting_days, curr_day, 7, FastingLevels.NO_FASTING)

### meatfare
curr_day += timedelta(weeks=2) # monday of meatfare
mark_range(fasting_days, curr_day, 7,FastingLevels.NO_MEAT)

### begin of great lent 
curr_day += timedelta(weeks=1)
while curr_day < easter_sunday-TD_ONE_DAY:
    fasting_days[curr_day] = FastingLevels.NO_OIL
    # on weekend oil is allowed
    if curr_day.weekday() in [5, 6]:
        fasting_days[curr_day] = FastingLevels.NO_FISH
    curr_day+=TD_ONE_DAY
fasting_days[easter_sunday-TD_ONE_DAY] = FastingLevels.NO_OIL
# christos anesti! during bright week no fasting
mark_range(fasting_days, easter_sunday, 7, FastingLevels.NO_FASTING)

# until pentecost wed and fri oil allowed
curr_day = easter_sunday+timedelta(weeks=1)
while curr_day < pentecost:
    if curr_day.weekday() in [2, 4]:
        fasting_days[curr_day] = FastingLevels.NO_FISH
    curr_day+=TD_ONE_DAY


#### pentecost
curr_day = pentecost
# no fasting during pentecost:
mark_range(fasting_days, curr_day, 7, FastingLevels.NO_FASTING)

#### apostles fast
# find monday after sunday of all saints, which is the next sunday after pentecost
while curr_day.weekday()!=1:
    curr_day+=TD_ONE_DAY
# mark fasting days:
while curr_day < feast_of_st_peter_paul:
    fasting_days[curr_day]=FastingLevels.NO_DAIRY
    if curr_day.weekday() in [2, 4]:
        fasting_days[curr_day]=FastingLevels.NO_OIL
    curr_day+=TD_ONE_DAY

#### fasting before dormition
curr_day = dormition_of_the_theotokos-timedelta(weeks=2)
while curr_day < dormition_of_the_theotokos:
    if curr_day.weekday() in [5, 6]:
        fasting_days[curr_day] = FastingLevels.NO_FISH
    else:
        fasting_days[curr_day] = FastingLevels.NO_OIL
    curr_day+=TD_ONE_DAY

#### fasting before christmas:
curr_day = christmas-timedelta(days=40)
while curr_day <= date(current_year,12,10):
    fasting_days[curr_day] = FastingLevels.NO_DAIRY
    curr_day+=TD_ONE_DAY
while curr_day <= min(christmas, last_day_of_year):
    if curr_day.weekday() in [0,2,4]:
        fasting_days[curr_day] = FastingLevels.NO_FISH
    else:
        fasting_days[curr_day] = FastingLevels.NO_OIL
    curr_day+=TD_ONE_DAY

for k,v in fasting_days.items():
    print(f"{k}: {v}")

# we're finished
if style == "new":
    exit(0)
curr_day = first_day_of_year
# we're on old calendar, but christmas moved after first day of year:
christmas = date(current_year-1,12,25)+timedelta(days=ORTHODOX_OFFSET_DAYS)
while curr_day < christmas:
    if curr_day.weekday() in [0,2,4]:
        fasting_days[curr_day] = FastingLevels.NO_FISH
    else:
        fasting_days[curr_day] = FastingLevels.NO_OIL
    curr_day+=TD_ONE_DAY