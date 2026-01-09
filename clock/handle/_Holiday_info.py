
import json
from typing import  Dict, List, Optional
from ..utils import db_to_message, message_to_db
from pathlib import Path
import requests
holiday_data = Path('./data/clocks/raw_holiday.json')

class HolidayHandle:
    def __init__(self, data_file: Path=holiday_data):
        self.data_file = data_file
        if not data_file.exists():
            self.get_requests()
        self.init_data
            
    
    def get_requests(self) -> List[Dict]:
        res = requests.get(url=f'https://api.apihubs.cn/holiday/get?year={2025}&cn=1&size=366')
        assert res.status_code == 200
        with open(self.data_file, 'w') as f:
            json.dump(res.json()['data']['list'], f, indent=4)
        
    
    def init_data(self):
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)