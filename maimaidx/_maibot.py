import requests
import random

class maimaibot:
    def __init__(self):
        url = 'https://maimaidx.herokuapp.com/maimai/songs'
        r = requests.get(url)
        self.data = r.json()['data']

        rank = ['6' ,'6+', '7', '7+', '8', '8+', '9', '9+', '10', '10+',
        '11', '11+' ,'12', '12+', '13', '13+', '14', '14+', '15']
        self.rank_dict = {}
        for k in rank:
            self.rank_dict[k]=list()
        self.get_lev_list()
        
    def get_lev_list(self):
        lev_rank=[
        'dx_lev_bas','dx_lev_adv', 'dx_lev_exp', 
        'dx_lev_mas', 'dx_lev_remas', 
        'lev_bas','lev_adv', 'lev_exp', 
        'lev_mas', 'lev_remas']
        data = self.data
        for index, song in enumerate(data):

            for lv_index, lev in enumerate(lev_rank):
                try:
                    if lev in song['jp'].keys():
                        self.rank_dict[song['jp'][lev]].append((index, lv_index))
                except:
                    pass          

    def random_lev(self, lev):
        new_lv_name = ['DX蓝', 'DX绿', 'DX红', 'DX紫', 'DX白', '蓝', '绿', '红', '紫', '白']
        data = self.data
        song, lv = random.choice(self.rank_dict[lev])
        title = data[song]['jp']['title']
        catcode = data[song]['jp']['catcode']
        jacket = data[song]['jp']['jacket']
        
        return (new_lv_name[lv]+' '+lev ,title,catcode ,jacket)