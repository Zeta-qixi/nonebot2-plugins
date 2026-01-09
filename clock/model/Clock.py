from ..utils import db_to_message, cron_to_natural

class Clock:
    def __init__(self, data):
        self.id = data['id']  # 主键，自增
        self.type = data.get('type', 'private')  # 聊天类型：'private' 或 'group'
        self.group_id = data.get('group_id')  # 群聊 ID（如果是群聊）
        self.user_id = data.get('user_id')    # 用户 ID（如果是私聊）
        self.content = data.get('content', '')  # 提醒内容
        self.is_enabled = bool(data.get('is_enabled', True))  # 是否启用任务
        self.cron_expression = data.get('cron_expression', '* * * * *')  # Cron 表达式
        self.is_one_time = bool(data.get('is_one_time', False))  # 是否只提醒一次
        

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'content': self.content,
            'is_enabled': int(self.is_enabled),
            'cron_expression': self.cron_expression,
            'is_one_time': int(self.is_one_time),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data)
    
    def set_id(self, id: int):
        self.id = id


    async def get_info(self):

        enabled = '✅' if self.is_enabled else '🚫'
        content = await db_to_message(self.content, only_show=True)
        ones = '（仅一次）' if self.is_one_time else ''
        return f"{enabled}|{cron_to_natural(self.cron_expression)}{ones}\n{content}"
    

