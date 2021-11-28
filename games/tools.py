from random import shuffle, choice
from nonebot.adapters.cqhttp.message import Message

class RouletteGame:
    '''
    俄罗斯转盘

    修改子弹
    开枪
    查看状态
    '''
    def __init__(self):
        
        self.set_bullet(0)
        self.filled = False
        self.member = []
        self.rule = '---指令列表---\n【填装（数字）】填装子弹\n【开枪】开一枪\n【结束】献祭一个🐎结束游戏'
        self.bullet = 0

    def set_bullet(self, nums):
        self.revolver = [0 for i in range(6)]
        for i in range(nums):
            self.revolver[i] = 1
        shuffle(self.revolver)

    def shoot(self):
        res = self.revolver[0]
        self.revolver.pop(0)
        return res

    def get_status(self):
        times = len(self.revolver)
        bullet = sum(self.revolver)

        return(times, bullet)

    def dead(self, id):
        pass
        #self.member[id] = 'dead'

    def random_shoot(self):
        return choice(self.member)
        
