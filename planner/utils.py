from datetime import datetime
from calendar import HTMLCalendar, month_name
from .models import Event, EventManager


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

    def formatweekname(self, theyear, themonth, starting_day):
        s = 'This Week'
        return '<tr><th colspan="7" class="%s"> <i class="fas fa-arrow-left"></i> %s <i class="fas fa-arrow-right"></i></th></tr>' % (
            self.cssclass_month_head, s)

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''

        for event in events_per_day:
            d += f"<li class='calendar_event'> <a href='/details/{event.id}''>{event.title}</a><p class='time'>{event.start_time.time } </p> </li >"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul> </td >"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formathour(self, theweek, events, year, month):
        day = ''
        first = theweek[0][0]
        print(theweek)

        def time(x):
            if x < 10:
                return '0'+str(x) + ':00'
            return str(x) + ':00'

        def row(x):
            row = ''
            j = events.last()
            for i in range(first, first+7):
                if j.start_time.hour == x and j.start_time.day == i:
                    print(j.start_time.hour)
                    print(j.start_time.day)
                    row += f"<td class='event'><a href='/details/{j.id}'> <span span id='{i}' >{j.title}</span></a></td>"
                else:
                    row += f"<td><span span id='{i}' class='hour'>{time(x)}</span></td>"
            return row
        for i in range(0, 24):
            day += f" <tr class='hour'><span class='hour'>{row(i)}</span></tr>"
        for d, weekday in theweek:
            self.formatday(d, events)

        return day

    def whole_month(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

    def whole_week(self, starting_day, year, month, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="week">\n'
        cal += f'{self.formatweekname(self.year, self.month, starting_day)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            if str(starting_day) in self.formatweek(week, events):
                cal += f'{self.formathour(week, events, year, month)}\n'

        return cal
