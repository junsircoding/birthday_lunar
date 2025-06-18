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

# 文件头
header = """BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
X-WR-CALDESC:亲友农历生日，由代码自行生成。
X-WR-CALNAME:亲友农历生日
CLASS:PUBLIC
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
END:STANDARD
END:VTIMEZONE
"""

# 文件结尾
tail = """END:VCALENDAR"""

# 事件模板
event = """BEGIN:VEVENT
SUMMARY:{summary}
DTSTART;VALUE=DATE:{dtstr_start}
DTEND;VALUE=DATE:{dtstr_end}
DTSTAMP;VALUE=DATE:{dtstr_start}
UID:{dtstr2_start}/{dtstr2_end}/NateScarlet/birthday-cn
END:VEVENT
"""

with open("lunar_birthdays_1900_2100.ics", "w") as f:
    f.write(header)

start_year = 1900
end_year = 2100
tz = pytz.timezone("Asia/Shanghai")

cal = Calendar()
cal.add("version", "2.0")

for name, lunar_month, lunar_day, is_leap, birth_year in birthdays:
    for year in range(max(start_year, birth_year), end_year + 1):
        try:
            lunar = Lunar(year, lunar_month, lunar_day, isleap=is_leap)
            solar = Converter.Lunar2Solar(lunar)
            age = year - birth_year
            summary = f"{name}{age}岁生日"
            dtstr_start = tz.localize(datetime(solar.year, solar.month, solar.day)).strftime("%Y%m%d")
            dtstr_end = (tz.localize(datetime(solar.year, solar.month, solar.day) + timedelta(days=1))).strftime("%Y%m%d")
            dtstr2_start = tz.localize(datetime(solar.year, solar.month, solar.day)).strftime("%Y-%m-%d")
            dtstr2_end = (tz.localize(datetime(solar.year, solar.month, solar.day) + timedelta(days=1))).strftime("%Y-%m-%d")
            # desc = f"{name}的农历生日：{'闰' if is_leap else ''}{lunar_month}月{lunar_day}日，年龄：{age}岁"
            
            with open("lunar_birthdays_1900_2100.ics", "a") as f:
                f.write(event.format(
                    summary=summary,
                    dtstr_start=dtstr_start,
                    dtstr_end=dtstr_end,
                    dtstr2_start=dtstr2_start,
                    dtstr2_end=dtstr2_end,
                    # desc=desc

                ))
        except DateNotExist:
            continue

with open("lunar_birthdays_1900_2100.ics", "a") as f:
    f.write(tail)