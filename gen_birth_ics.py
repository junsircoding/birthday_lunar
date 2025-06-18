from lunarcalendar import Converter, Lunar, DateNotExist
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import csv

birthdays = []
with open("birth.txt", mode='r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        if row['是否闰月'] == "是":
            birthdays.append((row['姓名'], int(row['农历月份']), int(row['农历日期']), True, int(row["出生年份"])))
        else:
            birthdays.append((row['姓名'], int(row['农历月份']), int(row['农历日期']), False, int(row["出生年份"])))
                             
print(birthdays)

start_year = 1900
end_year = 2100
tz = pytz.timezone("Asia/Shanghai")

cal = Calendar()
cal.add("prodid", "-//Lunar Birthday Calendar with Age//Jun//")
cal.add("version", "2.0")

for name, lunar_month, lunar_day, is_leap, birth_year in birthdays:
    for year in range(max(start_year, birth_year), end_year + 1):
        try:
            lunar = Lunar(year, lunar_month, lunar_day, isleap=is_leap)
            solar = Converter.Lunar2Solar(lunar)
            age = year - birth_year
            event = Event()
            event.add("summary", f"{name}{age}岁生日")
            event.add("dtstart", tz.localize(datetime(solar.year, solar.month, solar.day)))
            event.add("dtend", tz.localize(datetime(solar.year, solar.month, solar.day) + timedelta(days=1)))
            event.add("dtstamp", datetime.now(tz))
            event.add("description", f"{name}的农历生日：{'闰' if is_leap else ''}{lunar_month}月{lunar_day}日，年龄：{age}岁")
            cal.add_component(event)
        except DateNotExist:
            continue

with open("lunar_birthdays_1900_2100.ics", "wb") as f:
    f.write(cal.to_ical())
