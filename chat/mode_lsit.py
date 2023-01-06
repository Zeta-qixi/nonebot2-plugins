model_type = ['text-davinci-003', 'code-davinci-002']

class Mode:
    def __init__(
        self,
        mode_name: str,
        max_tokens:int = 150,
        temperature:float = 0,
        top_p:float = 1.0,
        frequency_penalty:float = 0.5,
        presence_penalty:float = 0.0,
        stop: list = ['me:', 'ai:'],
        prset: str = '',
        model_index: int = 0,
    ):
        self.mode_name = mode_name
        self.name = stop[1] if len(stop) > 1 else ''
        self.user = stop[0] if len(stop) > 0 else ''
        self.prset = prset
        self.mode = {
        'model': model_type[model_index],
        'max_tokens':max_tokens,
        'temperature': temperature,
        'top_p':top_p,
        'frequency_penalty':frequency_penalty,
        'presence_penalty':presence_penalty,
        }


atri_prest = """
me:现在你叫ATRI，是一个高性能机器人，之后的回答都要用atri代替“我”。
ATRI: atri很高兴能为您服务！atri可以为您做些什么？
"""


mode_list = [

Mode('ATRI', 150, 0.9, 1.0, 0, 0.6, ['me:', 'ATRI:'], atri_prest),
Mode('Base'),
Mode('chat',80, 0.5, 1.0, 0.5, 0,),
Mode('SQL_request', 100, 0.3, 1.0, 0, 0),
Mode('QA', 100, 0.3, 1.0, 0, 0),
Mode('story_creator', 60, 0.8, 1.0, 0.5, 0),
Mode('code_helper', 1024, 0, 1.0, 0.5 ,0,[] ,model_index=1)
]

