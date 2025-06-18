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
            birthdays.append((row['姓名'], int(row['农历月份']), int(row['农历日期']), True))
        else:
            birthdays.append((row['姓名'], int(row['农历月份']), int(row['农历日期']), False))
                             
print(birthdays)
# 生日列表
# birthdays = [
#     ("爸爸", 6, 4, False),
#     ("妈妈", 1, 14, False),
#     ("爷爷", 7, 17, False),
#     ("岳母", 7, 25, False),
#     ("我", 7, 26, False),
#     ("老婆", 8, 20, True),
#     ("岳父", 9, 19, False),
#     ("姣姣大舅", 11, 4, False),
#     ("高海娟", 12, 26, False),
#     ("瑞哥", 1, 4, False),
#     ("奶奶", 1, 24, False),
#     ("姐姐", 4, 5, False),
#     ("林泽亨孩子", 8, 31, False),
# ]

start_year = 1900
end_year = 2100
tz = pytz.timezone("Asia/Shanghai")

cal = Calendar()
cal.add("prodid", "-//Lunar Birthday Calendar//Jun//")
cal.add("version", "2.0")

for name, lunar_month, lunar_day, is_leap in birthdays:
    for year in range(start_year, end_year + 1):
        try:
            lunar = Lunar(year, lunar_month, lunar_day, isleap=is_leap)
            solar = Converter.Lunar2Solar(lunar)
            event = Event()
            event.add("summary", f"{name}18岁生日")
            event.add("dtstart", tz.localize(datetime(solar.year, solar.month, solar.day)))
            event.add("dtend", tz.localize(datetime(solar.year, solar.month, solar.day) + timedelta(days=1)))
            event.add("dtstamp", datetime.now(tz))
            event.add("description", f"{name}的农历生日：{'闰' if is_leap else ''}{lunar_month}月{lunar_day}日")
            cal.add_component(event)
        except DateNotExist:
            continue

with open("lunar_birthdays_1900_2100.ics", "wb") as f:
    f.write(cal.to_ical())
