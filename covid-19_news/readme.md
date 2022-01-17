# nonebot-plugin-covid19-news
国内新冠消息查询
「人在天津 单位在湘 家在广州 😭😭😭 」

## 安装使用
### 方法一 使用nb-cli
```
nb plugin install nonebot_plugin_covid19_news
```

### 方法二 使用pip
```
# pip 下载包
pip install nonebot_plugin_covid19_news


# 配置 pyproject.toml

plugins = [
    ...,
    "nonebot_plugin_covid19_news",
    ]

```


## 目前指令

### 查询地方疫情信息（风险等级 新增 目前确诊） 
指令: `城市名 + 疫情`  
事例: `天津疫情` 


### 查询地方出入政策  
指令: `城市名 + 疫情政策`  
事例: `广州疫情政策`

###  疫情信息定时推送
（9:00, 12:00, 21:00）推送到群内。 目前没保存到文件, 重启bot后会重置  
指令: `关注疫情 + 城市名`  
事例: `关注疫情 北京`



## 后续可能添加的功能
- 看需求添加更多疫情信息
- 从A市到B市 （A的出行政策和B的进入政策）
- 不知道有没有固定的更新时间，但这个无所谓
- 定时推送关注城市疫情信息
- 疫情风险等级变更提醒