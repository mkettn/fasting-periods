import logging
import jinja2
import minify_html
from FastingCalendar import FastingLevels, TD_ONE_DAY
from datetime import date, timedelta
from calendar import monthrange, day_abbr

_FL2HC = [ "f0", "f1", "f2", "f3", "f4", ]

class _MonthDisplay:
    def __init__(self, year:int, month:int, fastdays:dict, transl):
        days = []
        first_day_of_month = date(year, month, 1)
        last_day_of_month = date(year, month, monthrange(year, month)[1])
        last_day_in_table = last_day_of_month+timedelta(days=6-((last_day_of_month.weekday()+1)%7))
        curr_day = first_day_of_month
        if curr_day.weekday()!=6:
            curr_day = first_day_of_month-timedelta(days=first_day_of_month.weekday()+1)
        self.begin = None
        cnt = 0
        while curr_day <= last_day_in_table:
            if (curr_day < first_day_of_month) or (curr_day > last_day_of_month):
                days.append("empty")
            else:
                if self.begin is None:
                    self.begin = cnt
                days.append(_FL2HC[fastdays.get(curr_day, FastingLevels.NO_FASTING).value])
            curr_day += TD_ONE_DAY
            cnt+=1
        self.days = days
        self.name = transl["months"][first_day_of_month.month-1]

def fastdays2html(year, fastdays, transl, htmlfile, title="", introduction="", footer=""):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    tpl = env.get_template("calendar.jinja")
    months = []
    for m in range(1,13):
        months.append(_MonthDisplay(year, m,fastdays,transl))
    content = tpl.render(
        title=title, 
        introduction=introduction, 
        months=months,
        transl=transl,
        footer=footer
        )
    with open(htmlfile, 'w') as fd:
        fd.write(minify_html.minify(content))
