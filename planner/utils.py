from datetime import datetime, timedelta
from calendar import HTMLCalendar, month_name
from .models import Event


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="%s"> <i class="fas fa-arrow-left"></i> %s <i class="fas fa-arrow-right"></i></th></tr>' % (
            self.cssclass_month_head, s)

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li class="calendar_event"> <a href="/details/{event.id}">{event.title}</a> </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def whole_month(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

    def whole_week(self, starting_day, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        x = 0
        for week in self.monthdays2calendar(self.year, self.month):
            if str(starting_day) in self.formatweek(week, events):
                cal += f'{self.formatweek(week, events)}\n'

        return cal
