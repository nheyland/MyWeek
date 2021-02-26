from datetime import datetime, date, timedelta
from calendar import HTMLCalendar, month_name, day_abbr, weekday
from .models import Event, EventManager


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None, day=None):
        self.day = day
        self.year = year
        self.month = month
        self.date = date(year, month, day)

    def formatweekheaderdates(self, year, month, day, events):
        week_header_dates = ''
        theweek = ''
        for week in self.monthdays2calendar(self.year, self.month):
            if str(day) in self.formatweek(week, events):
                print(week)
                theweek = week
        x = self.itermonthdates(self.year, self.month)
        first = date(year, month, theweek[0][0])
        for i in x:
            if i == first:
                for j in range(0, 7):
                    week_header_dates += f"<td class='dow'>{str((i+timedelta(j)).month)}/{str((i+timedelta(j)).day)}</td>"
        return week_header_dates

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return f'<th class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day], day_abbr[day])

    def weekdays(self):
        pass

    def formatweekheader(self, start=False, month=False):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        x = f"<tr class='dow'>%s </tr>" % s
        return x

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="%s"> <i class="fas fa-arrow-left"></i> %s <i class="fas fa-arrow-right"></i></th></tr>' % (
            self.cssclass_month_head, s)

    def formatweekname(self):
        s = 'Week with ' + str(self.month) + '/' + \
            str(self.day) + '/'+str(self.year)
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
        first = date(year, month, theweek[0][0])

        def time(x):
            return ' '
            if x < 10:
                return '0'+str(x) + ':00'
            return str(x) + ':00'

        def row(x):
            row = ''
            date_arr = []
            for i in self.itermonthdates(self.year, self.month):
                if i == first:
                    for j in range(0, 7):
                        date_arr.append(i+timedelta(j))
            j = events.last()
            for i in date_arr:
                hold = 0
                for j in events.all():
                    if j.start_time.hour == x and j.start_time.day == i.day:
                        row += f"<td class='event'><a href='/details/{j.id}'> <span id='{i}' >{j.title}</span></a></td>"
                        hold += 1
                for j in events.all():
                    if j.start_time.hour < x and j.end_time.hour > x and j.start_time.day == i.day:
                        row += f"<td class='event_mid'></td>"
                        hold += 1
                for j in events.all():
                    if j.end_time.hour == x and j.end_time.day == i.day:
                        row += f"<td class='event_end'></td>"
                        hold += 1
                if hold == 0:
                    row += f"<td ><span id='{i}' class='hour'>{time(x)}</span></td>"
            return row
        for i in range(0, 24):
            if i % 2 == 0:
                day += f" <tr class='hour even'><span class='hour'>{row(i)}</span></tr>"
            else:
                day += f" <tr class='hour odd'><span class='hour'>{row(i)}</span></tr>"

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

    def whole_week(self, day, year, month, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="week">\n'

        cal += f'{self.formatweekname()}\n'
        cal += f'{self.formatweekheader()}\n'
        cal += f'{self.formatweekheaderdates(year, month, day, events)}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            if str(day) in self.formatweek(week, events):
                cal += f'{self.formathour(week, events, year, month)}\n'
        return cal
