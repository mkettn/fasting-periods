import logging
from FastingCalendar import FastingLevels, TD_ONE_DAY
from datetime import date, timedelta
from calendar import monthrange, day_abbr

def _write_month(year:int, month:int, fastdays:map, fd):
    fl2hc = {
        FastingLevels.NO_FASTING: "f0",
        FastingLevels.NO_MEAT: "f1",
        FastingLevels.NO_DAIRY: "f2",
        FastingLevels.NO_FISH: "f3",
        FastingLevels.NO_OIL: "f4",
    }
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, monthrange(year, month)[1])
    last_day_in_table = last_day_of_month+timedelta(days=6-((last_day_of_month.weekday()+1)%7))
    curr_day = first_day_of_month
    # move current day to last sunday
    if curr_day.weekday()!=6:
        curr_day = first_day_of_month-timedelta(days=first_day_of_month.weekday()+1)
    print(f'<table class="month"><tr><th colspan="7">{first_day_of_month.strftime("%B")}</th></tr><tr class="wd">', file=fd)
    for d in map(lambda x: x[:2].upper(), day_abbr):
        print(f'<th>{d}</th>', file=fd)
    print("</tr>", file=fd)
    while curr_day <= last_day_in_table:
        if curr_day.weekday()==6: # start new row each sunday
            print("<tr>", file=fd)
        if (curr_day < first_day_of_month) or (curr_day > last_day_of_month):
            print('<td class="empty"></td>', file=fd)
        else:
            print(f'<td class="{fl2hc[fastdays.get(curr_day, FastingLevels.NO_FASTING)]}">{curr_day.day}</td>', file=fd)
        if curr_day.weekday()==5: # end row each saturday
            print('</tr>', file=fd)
        curr_day += TD_ONE_DAY
    print('</table>', file=fd)


def fastdays2html(year, fastdays, transl, htmlfile, title="", introduction="", footer=""):
    with open(htmlfile, 'w') as fd:
        print(f'<!DOCTYPE html><html><head><title>{title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{introduction}<div class="grid">', file=fd)
        for m in range(1,13):
            _write_month(year,m,fastdays,fd)
        print(f'<div>{footer}</body></html>', file=fd)
