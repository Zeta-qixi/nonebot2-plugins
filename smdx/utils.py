

import datetime
import re
# 今天是几号星期
WEEK = ['一', '二', '三', '四', '五', '六', '日']
def get_weekday(date: str):
    print(date)
    if date[:2] == '今天':
        index = datetime.date.today().weekday()
    elif date[:2] == '明天':
        index = datetime.date.today().weekday()+1
    else:
        ret = re.search('(\d{4})?[-.年]?(\d{1,2})[-.月](\d{1,2})[日号]?', date)
        year, mouth, day = ret.groups()
        if not year:
            year = datetime.date.today().year
        index = datetime.date(int(year),int(mouth),int(day)).weekday()

    return WEEK[index]