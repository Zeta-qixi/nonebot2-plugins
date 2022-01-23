class Clock:
    def __init__(self, *args):
        args = args[0]
        self.id = args[0]
        self.type = args[1]
        self.user_id = args[2]
        self.content = args[3]
        self.time = args[4]
        self.ones = args[5]

        self.get_time()
    
    def get_info(self):
        ones=['重复', '一次']
        time_ = ' '.join([i for i in self.time.split() if i !='null'])
        return f'[{self.id}] ⏰{time_} ({ones[(self.ones)]})\n备注: {self.content}'

    def get_time(self):
        time = self.time.split()[-1].split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])