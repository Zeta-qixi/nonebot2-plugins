# 基于nonebot2的插件库
### 文件放到自己bot的插件目录即可，缺少的 data.json 或 data.db 请自行添加  
### 部分插件需要在nonebot的env中配置MASTER (qq号)
```
MASTER = [123456]

OCR_KEY = {"appId":"", "apiKey":"","secretKey": ""}

```

# 📝
- 一些仓库有的 但这里没写的为未完成插件  
- 部分插件没写readme （懒，如需要提一下）  
- 项目算是刚学python弄的（2018），所以不同插件的代码风格可能很大，如果觉得代码有些地方存在不合理的地方请提出来！ 


# 插件 

| 迁移状态 |      插件       |     简介       |
|:------:|:---------------:|:------------:|
| - [x] |  [国内疫情查询](https://github.com/Zeta-qixi/nonebot-plugin-covid19-news) | nonebot-plugin-covid19-news |
| - [x] |  [bilibili](./bilibili) | b站up直播提醒，动态转发 |
| - [x] |  [群管理](./atirbot) | bot添加好友 群管理 等等 |
| - [x] |  [简单对话](./chat) | 对话插件，支持 一问对多答，随机答，调整回复概率  |
| - [x] |  [rua](./rua) | 戳一戳群友rua头像，或者rua图片 |
| - [x] |  [搜图](./search_pic) | 搜图 参考 [hoshino项目](https://github.com/pcrbot/Hoshino-plugin-transplant/tree/master/image) |
| - [x] |  [setu](./setu) | 基于[pixivpy_async](https://github.com/Mikubill/pixivpy-async)的setu插件 |
| - [x] |  [涩图评分](./setu_score) | 度娘为你的色图打分～ |
| - [x] |  [日常实用功能](./smdx) | 目前有天气查询 星期几查询 .. |
| - [x] |  [简单的群内小游戏1](./games) | 俄罗斯转盘 开枪！ ｜
| - [x] |  [简单的群内小游戏2](./jrrp) | jrrp决斗版 ｜
| - [] |  [clock](./clock) | 闹钟、提示事项 |
| - [] |  [漫画更新提醒](./comic_push) | 还要找点目标网站爬 |
| - [] |  [插件管理](./block) | 修改block实现的关键字触发阻断, 从而实现类似插件管理的功能 |
| - [] |  [词语生成](./word_cloud) | 根据聊天记录生成词语, 无需log |
| - [] |  [maimaidx随歌](./maimaidx) | 舞萌街机随歌器 |