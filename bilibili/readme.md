(bilibili-api文档)[https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/user/info.md]  
# bilibili
- 推送b站主播直播信息到群聊  
- 推送动态(不包含转发)  
- 对动态进行过滤式推送(如 只推送公告)
# 使用前需要做的
### 1. 在插件目录下创建DB文件 `data.db`

### 2. 创建表
```sql
CREATE TABLE bilibili(  
    id int primary key AUTOINCREMENT,
    gid INTEGER not null,     -- 群id
    mid INTEGER not null,     -- b站id
    name char(50),            -- 主播名称
    live INTEGER,             --（0 or 1）是否推送直播消息
    is_live INTEGER,          -- 直播状态
    dynamic INTEGER,          --（0 or 1）是否推送动态消息
    latest_dynamic INTEGER,   -- 最新动态时间
    dy_filter char(50),       -- 动态过滤字段 （过滤没有该字段的动态）
    primary key(gid, mid)     -- 联合主键, 对于sqlite而言 没什么用
);
```


# 主要指令 （无需@）
### 1. `添加关注 mid`  
  - 关注主播，推送直播信息，但不推送动态信息
### 2. `取消关注 mid`  
  - 取消关注主播（不推送信息 但不会删除主播在数据库的数据）
### 3. `更新推送 mid (动态|直播|过滤) ([0,1]|[0,1]|['过滤字段'])`  
```python
"更新推送 mid 直播 0" # 停止推送主播直播信息
"更新推送 mid 动态 1" # 推送主播动态信息
"更新推送 mid 过滤 公告" # 只推送主播含‘公告’字段的动态信息
```
    

