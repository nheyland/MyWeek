from datetime import datetime, date, timedelta
from calendar import HTMLCalendar,  month_name, day_abbr
import time
from .models import Event, User


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None, day=None):
        self.day = day
        self.year = year
        self.month = month
        self.date = date(year, month, day)

    def dow_date_format(self, year, month, day):
        week_header_dates = ''
        week = ''
        for i in Calendar.monthdatescalendar(self, year, month):
            for j in i:
                if self.date == j:
                    week = i
        for j in week:
            week_header_dates += f"<td class='dow'>{j.month}/{j.day}</td>"
        return week_header_dates

    def dow(self, start=False, month=False):
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

    def day_picker(self, weeks_out):
        s = ''
        if weeks_out == 0:
            s = 'This Week'
        elif weeks_out == 1:
            s = f'{weeks_out} Week Out'
        else:
            s = f'{weeks_out} Weeks Out'
        prev = weeks_out - 1
        next = weeks_out + 1
        if prev < 0:
            prev = 0
        return f'<tr><th colspan="7" class="%s"> <a href="/planner/{prev}" <i class="fas fa-arrow-left"></i></a> %s <a href="{next}" <i class="fas fa-arrow-right"></i></a></th></tr>' % (
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

    def formathour(self, week, events, year, month):
        day = ''
        print(week)
        first = date(year, month, week[0][1])

        def row(x):
            row = ''
            date_arr = []
            week = ''
            for i in Calendar.monthdatescalendar(self, year, month):
                for j in i:
                    if self.date == j:
                        date_arr = i
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
                    row += f"<td ><span id='{i}' class='hour'>   </span></td>"
            return row
        for i in range(0, 24):
            if i % 2 == 0:
                day += f" <tr class='hour even'><span class='hour'>{row(i)}</span></tr>"
            else:
                day += f" <tr class='hour odd'><span class='hour'>{row(i)}</span></tr>"

        for d, weekday in week:
            self.formatday(d, events)

        return day

    def whole_month(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.dow()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

    def whole_week(self, day, year, month, id):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="week">\n'
        cal += f'{self.day_picker(id)}\n'
        cal += f'{self.dow()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            for i in week:
                if i[0] == day:
                    cal += f'{self.dow_date_format(year, month, day)}\n'
                    cal += f'{self.formathour(week, events, year, month)}\n'
        return cal


class Time_return:

    def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()

    def dst(request):
        tz = {
            'dls': {
                'est': 4,
                'cnt': 5,
                'mtn': 6,
                'pcf': 7
            },
            'std': {
                'est': 5,
                'cnt': 6,
                'mtn': 7,
                'pcf': 8
            }
        }
        d = Time_return.get_date(request.GET.get('day', None))
        svg = 'dls' if time.localtime().tm_isdst < 0 else 'std'
        zone = User.objects.get(id=request.session['user_id']).tz if hasattr(
            User.objects.get(id=request.session['user_id']), 'tz') else 'est'

        return d-timedelta(hours=tz[svg][zone])
