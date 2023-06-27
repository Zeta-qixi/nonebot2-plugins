class mc_status:
    
    def __init__(self,address):
        
        self.address = address
        self.ping: float = 0
        self.running: bool = False
        self.online: int = 0
        self.version: str = ''
        self.platforms: str = ''
        self.player_list: list = ['']


    @property
    def info(self):
        
        _info = f"{self.platforms} {self.version}\n{self.address}\n在线人数: {self.online}"
        _status = "【开启】" + '\n'.join(self.player_list) if self.running else "【关闭】"
        return _info + _status
    
    
    def __str__(self):
        return self.info
    
    
    
class mcje_status(mc_status):
    def __init__(self,address):
        super().__init__(address)
        self.platforms = 'Java'
        
        
class mcbe_status(mc_status):
    def __init__(self,address):
        super().__init__(address)
        self.platforms = 'Bedrock'