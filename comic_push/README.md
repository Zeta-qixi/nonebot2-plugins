## 漫画更新推送
### 说明
爬取对漫画网站的信息, 对比本地数据进行更新推送。 目前爬取的网站没几个...

### 使用说明
1. 先进去找要继续推送的漫画
2. 获取url上的id  (比如`/50bz/`)
3. 私聊bot `manga 50bz` `copymanga dianjuren`


### data.json格式
www.mangabz.com
```
{
    "qq号": {
        "漫画id" : "最新话"
    }
}
```

www.copymanga.site
```
{
    "qq号": {
        "漫画id" : "最新更新时间"
    }
}
```
## 后续工作
- 找更多网站  
- 统一交互方式

