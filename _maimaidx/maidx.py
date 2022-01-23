import os
import json
import pandas as pd
from nonebot.adapters.onebot.v11.message import MessageSegment
class maibot:
    def __init__(self):
        gpath =os.path.dirname(__file__)
        self.dx = pd.read_csv( gpath+'/data/dx2021.csv')
        self.rank = ['dx_lev_bas','dx_lev_adv','dx_lev_exp', 'dx_lev_mas','dx_lev_remas','lev_bas','lev_adv','lev_exp', 'lev_mas','lev_remas']
        self.num_rank = ['6' ,'6+', '7', '7+', '8', '8+', '9', '9+', '10', '10+', '11', '11+' ,'12', '12+', '13', '13+', '14', '14+', '15']
        self.rank_color = {'bas': '🟢', 'adv': '🟡', 'exp': '🔴', 'mas': '🟣', 'remas': '⚪️'}
        #rank = {'B': '🟢BASIC', 'A': '🟡ADVANCED', 'E': '🔴EXPERT', 'M': '🟣MASTER', 'R': '⚪️RE:MASTER'}
        self.classes_list = {
        'niconicoボーカロイド':'niconico & VOCALOID', 
        'POPSアニメ':'流行 & 动漫', 
        '東方Project':'东方Project',
        'ゲームバラエティ':'其他游戏', 
        'maimai':'舞萌',
        'オンゲキCHUNITHM':'音击/中二节奏'
        }


    def get_song(self, lv:str) -> pd.DataFrame:
        '''
        按等级获取所有谱
        '''
        df = pd.DataFrame()
        for R in self.rank:
            df1 = self.dx[self.dx[R]==lv]
            df1['rank'] = R
            df = df.append(df1)
        
        
        return df

    def random_song(self, lv:list, num:int=1, rank:str=None):
        '''
        随机歌曲
        '''
 
        df = self.get_song(lv[0])

        #按等级范围随歌
        if len(lv) == 2:
            i = self.num_rank.index(lv[0])+1
            j = self.num_rank.index(lv[1])+1
            for lv in self.num_rank[i:j]:
                df = df.append(self.get_song(lv))

        #规定颜色
        if rank :
            df = df[(df['rank'] == self.rank[rank]) | (df['rank'] == self.rank[rank+5])]

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
            if 'dx' in item['rank']:
                rank = '[DX]'
            else :
                rank = '[标准]'

            for R in self.rank_color.keys():
                if R in str(item['rank']).split('_'):
                    rank = rank + self.rank_color[R]
                    break

            rank = rank +' '+ item[item['rank']]
            img = MessageSegment.image(file=item['jacket'])
            msg.append(f"【{self.classes_list[item['catcode']]}】\n『{item['title']}』\n" + img + f"\n{rank}")
        return msg