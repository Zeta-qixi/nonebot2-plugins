参考文档 (bilibili-api文档)[https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/user/info.md]  

## 需要用到qlite3
#### 目录下创建`data.db`
#### 创建表
```
CREATE TABLE bilibili(  
    gid INTEGER not null,
    mid INTEGER not null,
    name char(50),
    live INTEGER,
    dynamic INTEGER,
    latest_dynamic INTEGER,
    dy_filter char(50),
    primary key(gid, mid)
);
```
## 使用方法
`添加关注 mid`  
`取消关注 mid`  
`更新推送 mid` `(动态|直播|过滤)` `([0,1],[0,1],['过滤字段'])`  

