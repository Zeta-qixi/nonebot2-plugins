import datetime
class Clock:
    def __init__(self, data):
        self.id = data['id']
        type = data.get('type', 'private')
        user = data.get('user')
        content = data.get('content', '')
        mouth = data.get('mouth', 0)
        day = data.get('day', 0)
        week = data.get('week', '')
        ones = data.get('ones', 1)
        time = data.get('time', 1)
        self.get_time()

    @classmethod
    def init_from_db(self, *args):
        args = args[0]
        self.id = args[0]
        self.type = args[1]
        self.user_id = args[2]
        self.content = args[3]
        self.month = args[4]
        self.day = args[5]
        self.week = args[6]
        self.time = args[7]
        self.ones = args[8]
        self.get_time()
    
    def get_info(self):
        ones=['重复', '一次']
        time_ = ' '.join([i for i in self.time.split() if i !='null'])
        return f'[{self.id}] ⏰{time_} ({ones[(self.ones)]})\n备注: {self.content}'

    def get_time(self):
        time = self.time.split()[-1].split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])


    def verify_today(self):

        if self.week and str(datetime.date.today().weekday()) not in self.week:
            return False

        if self.month > 0 and self.month != datetime.date.today().month:
            return False

        if self.day > 0 and self.day != datetime.date.today().day:
            return False

        return True
