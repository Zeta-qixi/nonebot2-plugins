#  因为腾讯云 阿里云 屏蔽了pixiv.cat 改用为[pixiv_api](https://github.com/Mikubill/pixivpy-async)

## 插件是直接爬去pixiv网站的，需要用到代理

## 关于 data.json PROXY 与 TOKEN
TOKEN为p站的`refresh_token` 在网页登陆pixiv账号 然后 `f12` 自己找就好  
- 如果有pixiv会员账号 请修改`pixiv_api.py`第13行的 `VIP = True`  
- 如果没有vip账号 建议添加多个账号  
./data.json
```json
 
{
    "PROXY": "你的代理服务器",
    "TOKEN": {
        "setu1" : "o-HYGiZqb****ny7RSwX7**********UD9He9Vgk",
        "setu2" : "-AJFpYE****DdbRS*********UJq_tBmgXRJFNY4",
        "setu3" : "pYjbX65N****qXO1D2O********xKaEa2itntWIqvQaHA",
        "no_r18" : "XMRudbQvup****u3N19K************ujTvt0NQ"
    }
}
```
## 关于data
该插件会下载setu原图到`data/image`  
`data/nosese`是撤回setu后随机发送的  

## 功能
### 基础色图功能
`setu  keyword nums`   
- keyword: 搜索标签或tags, 默认为 day_male  
- nums: setu数量, 默认 1, 限制<=3

如果 `keyword` 在 `tags` 中, 则是推荐setu 否则就是标签搜索setu  
多个标签用 ` ` 分格, 部分标签可能需要使用日文
```
tags:
"day", "week", "month", 
"day_male", "day_female", 
"week_original", "week_rookie", 
"day_r18", "day_male_r18", "day_female_r18", 
"week_r18", "week_r18g",

```
### 画师作品
`setu画师 name nums` or `setu作者 name nums`  
- name: 画师的 pixivID或名称  

### 推荐作品
`setu推荐 id nums`  
- id: pixiv作品ID

### 作品搜索
`setu搜索 id` or `setu搜图 id`
- id: pixiv作品ID  

用于与搜图插件配合

### 色图撤回
`撤回` `太色了` `太涩了`  
会撤回 该成员对应的setu 信息, 并发动不可以色色
