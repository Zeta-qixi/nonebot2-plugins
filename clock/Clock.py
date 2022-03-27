import datetime
from nonebot import logger
class Clock:
    def __init__(self, data):
 
        self.id = data['id']
        self.type = data.get('type', 'private')
        self.user = data.get('user')
        self.content = data.get('content', '')
        self.month = data.get('month', 0)
        self.day = data.get('day', 0)
        self.week = data.get('week', '')
        self.ones = data.get('ones', 1)
        self.time = data.get('time', 1)
        self.get_time()

    @classmethod
    def init_from_db(cls, *args):
        args = args[0]
        data = {}
        data['id'] = args[0]
        data['type'] = args[1]
        data['user'] = args[2]
        data['content'] = args[3]
        data['month'] = args[4]
        data['day'] = args[5]
        data['week'] = args[6]
        data['time'] = args[7]
        data['ones'] = args[8]
        return cls(data)
    
    def get_info(self):
        ones=['重复', '一次']
        time_ = ' '.join([i for i in self.time.split() if i !='null'])
        return f'[{self.id}] ⏰{time_} ({ones[(self.ones)]})\n备注: {self.content}'

    def get_time(self):
        time = self.time.split()[-1].split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])


    def verify_today(self):

        if self.week and str(datetime.date.today().weekday()+1) not in self.week:
            return False

        if self.month > 0 and self.month != datetime.date.today().month:
            return False

        if self.day > 0 and self.day != datetime.date.today().day:
            return False

        return True
