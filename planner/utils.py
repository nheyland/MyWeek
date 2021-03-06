
from datetime import datetime, date, timedelta, timezone
from calendar import HTMLCalendar,  month_name
from .models import Event, User
import requests as r
import time
import json
import pytz
import pickle


class Calendar(HTMLCalendar):

    def __init__(self, request, year=None, month=None, day=None, week=0, time_start=0, time_end=24):
        self.day = day
        self.year = year
        self.month = month
        self.date = date(year, month, day)
        self.week = week
        self.time_start = time_start
        self.time_end = time_end
        self.events = Event.objects.filter(
            created_by=User.objects.get(id=request.session['user_id']), start_time__year=self.year)
        self.attending = User.objects.get(
            id=request.session['user_id']).invited_to.all()

    def dow_date_format(self, year, month, day):
        week_header_dates = ''
        week = ''
        for i in Calendar.monthdatescalendar(self, year, month):
            for j in i:
                if self.date == j:
                    week = i
        for j in week:
            week_header_dates += f"<td class='dow '>{j.month}/{j.day}</td>"
        return week_header_dates

    def dow(self, month=False):
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        if month:
            return f"<tr class='dow'>%s </tr>" % s
        return f"<tr class='dow week'><td>%s</td></tr>" % s

    def formatmonthname(self, theyear, themonth):
        s = '%s %s' % (month_name[themonth], theyear)
        return '<tr ><th colspan="7" class="%s">  %s </th></tr>' % (
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
        return f'<tr><th colspan="8" class="%s"><p class="this_week"> <a href="/planner/{prev}" <i class="arrow fas fa-arrow-left"></i></a>  %s <a href="{next}" <i class="arrow fas fa-arrow-right"></i></a></p> </th></tr>' % (
            self.cssclass_month_head, s)

    def history():
        return 'yes'

    def formatday(self, day, events):
        events_per_day = events.filter(
            start_time__day=day, start_time__month=self.month)
        d = ''
        for event in events_per_day:
            d += f"<li class='calendar_event'> <a href='/details/{event.id}''>{event.title}</a><p class='time'>{event.start_time.time } </p> </li >"
        if day != 0:
            return f"<td class='week_full'><span class='date'>{day}</span><ul> {d} </ul> </td >"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formathour(self, week, events, attend, year, month, time_start, time_end):
        big_row = ''

        def row(x):
            row = ''
            date_arr = []
            for i in Calendar.monthdatescalendar(self, year, month):
                for j in i:
                    if self.date == j:
                        date_arr = i

            for i in date_arr:
                hold = 0
                for j in events:
                    if j.start_time.hour == x and j.start_time.day == i.day and j.start_time.month == i.month:
                        row += f"<td class='event event_start'><a href='/details/{j.id}'>{j.title}</a></td>"
                        hold += 1
                for j in attend:
                    if j.start_time.hour == x and j.start_time.day == i.day and j.start_time.month == i.month:
                        print('yes')
                        row += f"<td class='event attend_start'><a href='/details/{j.id}'>{j.title}</a></td>"
                        hold += 1

                for j in events:
                    if j.start_time.hour < x and j.end_time.hour > x and j.start_time.day == i.day and j.start_time.month == i.month:
                        row += f"<td class='event event_mid'></td>"
                        hold += 1
                for j in attend:
                    if j.start_time.hour < x and j.end_time.hour > x and j.start_time.day == i.day and j.start_time.month == i.month:
                        row += f"<td class='event attend_mid'></td>"
                        hold += 1
                for j in events:
                    if j.end_time.hour == x and j.end_time.day == i.day and j.start_time.month == i.month:
                        row += f"<td class='event event_end'></td>"
                        hold += 1
                for j in attend:
                    if j.end_time.hour == x and j.end_time.day == i.day and j.start_time.month == i.month:
                        row += f"<td class='event attend_end'></td>"
                        hold += 1
                if hold == 0:

                    row += f"<td id='{i} {x}' class='hour'>  </td>"
            return row

        def bettertime(t):
            if t == 12:
                return '12:00 PM'
            if t < 12:
                if t == 0:
                    return f'12:00 AM'
                return f'{t}:00 AM'
            else:
                t = t-12
                return f'{t}:00 PM'
        for i in range(time_start, time_end):
            if i % 2 == 0:
                big_row += f" <tr class='hour even'><td class='time'>{bettertime(i)}</td><span class='hour'>{row(i)}</span></tr>"
            else:
                big_row += f" <tr class='hour odd'><td class='time'>{bettertime(i)}</td><span class='hour'>{row(i)}</span></tr>"
        return big_row

    def whole_month(self):
        events = self.events
        cal = f'<table id="calendar" border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month)}\n'
        cal += f'{self.dow(month=True)}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

    def whole_week(self):
        self.setfirstweekday(6)
        events = self.events
        attend = self.attending
        for i in attend:
            print(i.title)

        print('And')
        for i in events:
            print(i.title)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" id="week" class="week">\n'
        cal += f'{self.day_picker(self.week)}\n'
        cal += f'<tr><th colspan="8" class="%s"> </th></tr>\n'
        cal += f'{self.dow()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            for i in week:
                if i[0] == self.day:
                    cal += f"<td class='dow'>Time</td>{self.dow_date_format(self.year, self.month, self.day)}\n"
                    cal += f'{self.formathour(week, events, attend, self.year, self.month, self.time_start, self.time_end)}\n'
        return cal


class Tools:

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
        d = Tools.get_date(request.GET.get('day', None))
        svg = 'dls' if time.localtime().tm_isdst < 0 else 'std'
        zone = User.objects.get(id=request.session['user_id']).tz if hasattr(
            User.objects.get(id=request.session['user_id']), 'tz') else 'est'
        return d-timedelta(hours=tz[svg][zone])

    def geocode(x):
        try:
            y = r.get('https://api.mapbox.com/geocoding/v5/mapbox.places/' + x +
                      '.json?access_token=pk.eyJ1IjoibmhleWxhbmQiLCJhIjoiY2toZHI4ZWNqMDgwaTMwczFuNnpvcGFuMiJ9.4LH3G0a18_HQY8t55W83lg').json()
            return y['features'][0]['center']
        except:
            return None

    def weather(latitude, longitude, time):

        OPEN_WEATHER = pickle.load(open("weather.p", "rb"))

        unix_time = int(
            (time - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds())
        response = r.get(
            f'http://api.openweathermap.org/data/2.5/onecall?lat={str(latitude)}&lon={str(longitude)}&dt={str(unix_time)}&appid={OPEN_WEATHER}&units=imperial')

        json_data = json.loads(response.text)
        daily_data_full = json_data['daily'][0]
        new_day = datetime.utcfromtimestamp(
            int(daily_data_full['dt'])).strftime('%Y-%m-%d %H:%M:%S')
        new_day = datetime.fromisoformat(new_day)
        event_weather_data = {}
        event_weather_data['dt'] = pytz.utc.localize(new_day)
        event_weather_data['day_temp'] = daily_data_full['temp']['day']
        event_weather_data['night_temp'] = daily_data_full['temp']['night']
        event_weather_data['main'] = daily_data_full['weather'][0]['main']
        event_weather_data['desc'] = daily_data_full['weather'][0]['description']
        event_weather_data['icon'] = daily_data_full['weather'][0]['icon']

        return event_weather_data
