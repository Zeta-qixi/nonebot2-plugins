import math
import random

from typing import List
from collections import defaultdict

class Player:
    def __init__(self, id, rp):
        
        self.name = f"[CQ:at,qq={id}]"
        self.HP = 30 
        self.atk = 10 + rp
        self.defence = 10 + rp / 10
        self.dodge = 0
        self.hit = 1
        self.rp = rp

        self.dodge = rp / 500

        if rp > 50:
            self.HP += math.ceil((rp - 50)/5)

        if rp >= 80:
            self.atk *= (1 + (rp - 70)/100)
            self.hit *= (1 + (rp - 70)/100)
            

    def attack(self, p) -> int:
        if random.random() < (self.hit - p.dodge):
            return ((100 + self.atk) / p.defence)
        return False

    def get_hurt(self, damage):
        self.HP -= damage
        return self.HP

    @property
    def live(self):
        if self.HP > 0:
            return round(self.HP, 2)
        return 0

class JrrpGame(dict):

    def add_player(self, id, rp):
        self[id] = Player(id, rp)



    def duel(self, p1, p2) -> List:

        if p1 not in self:
            return (["你还没jrrp呢"])

        if p2 not in self:
            return (["对方今天还没jrrp"])

        if not self[p1].live:
            return (["你已经4⃣️了 等明天再jrrp吧"])

        if not self[p2].live:
            return (["对方已经4⃣️了"])

        p1 = self[p1]
        p2 = self[p2]

        res = []
        round_ = 0
        while(p1.live and p2.live):
            round_ += 1
            if round_ == 3:
                
                break

            def atk(p1, p2):
                msg = f"{p1.name} 发起攻击"
                
                if damage:=p1.attack(p2):
                    msg += (f" 攻击命中🎯")
                    damage = (damage * (1+round_/10)) + random.randint(0, 3)
                    if random.random() < 0.1:
                        rate = round(1 + random.randint(50, 100)/100, 2)
                        msg += (f"\n本次攻击造暴击(x{rate})💥 ")
                        damage *= rate

                    damage = round(damage, 2)
                    msg += f"造成{damage}伤害🗡"
                    p2.get_hurt(damage)

                else:

                    msg += (f"  攻击被闪避了")
                res.append(msg)

                print(p1.name, damage, p2.HP)

            atk(p1, p2)
            atk(p2, p1)

            def if_live(live):
                return "" if live else "-> ☠️"
            res.append(f"{p1.name} 🩸{p1.live}{if_live(p1.live)}\n{p2.name} 🩸{p2.live}{if_live(p2.live)}")

        res.append('本次对决结束～')

        return res
            