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

# FIXME(mke): calculate offset to gregorian calendar day
TD_JUL_GREG = timedelta(days=13)

def mark_range(fc:map, start:datetime.date,days:int, lvl:FastingLevels):
    """ mark range in fasting calendar"""
    cd = start
    for _ in range(days):
        fc[cd] = lvl
        cd+=TD_ONE_DAY

def getFastingCalendar(year, old_style):
    first_day_of_year = date(year, 1,1)
    last_day_of_year = date(year, 12,31)
    offset = timedelta()
    if old_style:
        offset = TD_JUL_GREG
    ## fixed feast days:
    christmas = date(year, 12, 25)+offset
    theophany = date(year, 1, 6)+offset
    annunciation_of_the_theotokos = date(year, 3, 25)+offset
    dormition_of_the_theotokos = date(year, 8, 15)+offset
    nativity_of_the_theotokos = date(year, 9, 8)+offset
    feast_of_st_peter_paul = date(year, 6, 29)+offset
    # moving feast days:
    easter_sunday = easter(year, EASTER_ORTHODOX)
    ascension_of_christ = easter_sunday+timedelta(days=40)
    pentecost = easter_sunday+timedelta(days=50)
    # map for all days of current year -> FastingLevels:
    fasting_days = {}
    curr_day = theophany
    # fasting every wed and fri, except between christmas and thephany
    while curr_day < christmas:
        if curr_day.weekday() in [2,4]:
            fasting_days[curr_day] = FastingLevels.NO_OIL
        else:
            fasting_days[curr_day] = FastingLevels.NO_FASTING
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
    # fish allowed at the day of the announciation of the theotokos 
    if fasting_days[annunciation_of_the_theotokos]:
        fasting_days[annunciation_of_the_theotokos] = FastingLevels.NO_DAIRY
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
    curr_day+=timedelta(days=7)
    #### apostles fast
    # find monday after sunday of all saints, which is the next sunday after pentecost
    while curr_day.weekday()!=0:
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
    while curr_day <= date(year,12,10):
        fasting_days[curr_day] = FastingLevels.NO_DAIRY
        curr_day+=TD_ONE_DAY
    while curr_day <= min(christmas, last_day_of_year):
        if curr_day.weekday() in [0,2,4]:
            fasting_days[curr_day] = FastingLevels.NO_FISH
        else:
            fasting_days[curr_day] = FastingLevels.NO_OIL
        curr_day+=TD_ONE_DAY
    # we're finished
    if not old_style:
        return fasting_days
    # if we're on old calender, we're not finished yet
    curr_day = first_day_of_year
    # christmas moved after first day of year:
    christmas = date(year-1,12,25)+TD_JUL_GREG
    while curr_day < christmas:
        if curr_day.weekday() in [0,2,4]:
            fasting_days[curr_day] = FastingLevels.NO_FISH
        else:
            fasting_days[curr_day] = FastingLevels.NO_OIL
        curr_day+=TD_ONE_DAY
    return fasting_days