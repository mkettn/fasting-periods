import logging
from vobject import iCalendar
from FastingCalendar import FastingLevels

def fastdays2ics(fastdays, transl, icsfile):
    cal = iCalendar()
    for k, v in fastdays.items():
        if v == FastingLevels.NO_FASTING:
            continue
        e = cal.add('vevent')
        e.add('summary').value = transl[v]
        e.add('dtstart').value = k
    with open(icsfile, 'w') as f:
        f.write(cal.serialize())