import os
import json
import pandas as pd
from nonebot.adapters.cqhttp.message import MessageSegment
class maibot:
    def __init__(self):
        gpath =os.path.dirname(__file__)
        self.dx = pd.read_csv( gpath+'/data/dx2021.csv')
        self.rank = ['dx_lev_bas','dx_lev_adv','dx_lev_exp', 'dx_lev_mas','dx_lev_remas','lev_bas','lev_adv','lev_exp', 'lev_mas','lev_remas']
        self.rank_color = {'bas': '🟢BASIC', 'adv': '🟡ADVANCED', 'exp': '🔴EXPERT', 'mas': '🟣MASTER', 'remas': '⚪️RE:MASTER'}

    def get_song(self, lv:str) -> pd.DataFrame:
        '''
        按等级获取所有谱
        '''
        df = pd.DataFrame()
        for R in self.rank:
            df1 = self.dx[self.dx[R]==lv]
            df1['rank'] = R
            print(len(df1))
            df = df.append(df1)
        
        
        return df

    def random_song(self, lv:str, num:int=1, rank:str=None):
        '''
        随机歌曲
        '''
        df = self.get_song(lv)
        if rank :
            df = df[df['rank']==rank]

        if len(df) <= num :
            num = len(df)

        df = df.sample(num)
        return self.df2info(df)

    def df2info(self, data):
        
        '''
        将df数据转换为bot输出的Message
        '''
        msg = []

        for item in data.iterrows():
            item = item[1]

            for R in self.rank_color.keys():
                if R in item['rank']:
                    rank = self.rank_color[R]
                    break
            img = MessageSegment.image(file=item['jacket'])
            msg.append(f"【{item['catcode']}】\n{item['title']}\n" + img + f"\n{rank}")
        return msg