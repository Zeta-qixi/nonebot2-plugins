import random
import json
import os


class maimaidxbot:
    def __init__(self):
        gpath =os.path.dirname(__file__)
        path = gpath+'/data/maimaidxCN.json'
        with open(path) as f:
            self.data = json.load(f)['曲目列表']

        # rank = ['6' ,'6+', '7', '7+', '8', '8+', '9', '9+', '10', '10+',
        # '11', '11+' ,'12', '12+', '13', '13+', '14', '14+']
        # self.rank_dict = {}
        # for k in rank:
        #     self.rank_dict[k]=list()
        # self.get_lev_list()
        
    def get_songIndex_by_lv(self,**k):
        lv = k['lv']
        num = k['num']

        data = self.data

        # 将指定等级添加到list中
        song_index_list = []
        for index, song in enumerate(data):
            R = self.get_keys(song['等级'], lv)
            for r in R:
                
                if 'rank' in k.keys():
                    #指定RANK
                    if r == k['rank']:
                        song_index_list.append((index, r))
                else:
                    song_index_list.append((index, r))
        if len(song_index_list) < num:
            num = len(song_index_list)
            print('buguo')

        #随机发送
        return (self.index2info(random.choices(song_index_list,k = num)))#list

    def index2info(self, index_list):
        song_list = []
        
        rank = {'B': '🟢BASIC', 'A': '🟡ADVANCED', 'E': '🔴EXPERT', 'M': '🟣MASTER', 'R': '⚪️RE:MASTER'}

        classes_list = {
        'niconico':'niconico & VOCALOID', 
        'pops_anime':'流行 & 动漫', 
        'toho':'东方Project',
        'variety':'综艺节目', 
        'original':'原创乐曲'}

        for index, R in index_list:
            song = self.data[index]
            classes = classes_list[song['分类']]
            name = song['曲名']
            type = song['类型']
            cover = song['封面']
            song_list.append([classes, name, type, rank[R], cover])
        return song_list

            
            
    def get_keys(self, d, value):
        return [k for k,v in d.items() if v == value]