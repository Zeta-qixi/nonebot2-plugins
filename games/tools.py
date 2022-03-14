from random import choice, shuffle
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
        self.rule = '---指令列表---\n【填装（数字）】填装子弹\n【开枪】开一枪\n【决斗】 @一个人 开启solo模式\n【结束】献祭一个🐎结束游戏'
        self.bullet = 0
        self.duel = False

    def set_bullet(self, nums):
        self.revolver = [0 for i in range(6)]
        for i in range(nums):
            self.revolver[i] = 1
        shuffle(self.revolver)
        self.member = []
        self.duel = False


    def set_duel(self, id, id2):
        self.member = [id, id2]
        self.duel = True

    def shoot(self):
        res = self.revolver[0]
        self.revolver.pop(0)
        return res

    def get_status(self):
        times = len(self.revolver)
        bullet = sum(self.revolver)

        return(times, bullet, self.duel)

    def get_member(self):
        return self.member
    def dead(self, id):
        pass
        #self.member[id] = 'dead'

    def random_shoot(self):
        return choice(self.member)
        
