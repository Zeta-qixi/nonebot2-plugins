# 实用功能

## 添加文件
需要添加`./asset/data.json`  
```json
{
    "key": "",
    "city":{

    }
}
```

## 指令
### 设置天气位置

```
setcity = on_command('设置天气城市',)
```
`设置天气城市 广州`

### 天气查询
```
# matcher
on_regex('(.*)天气|气温|多少度|几度')
```
`广州天气`  `北京温度` `天气`...




api 返回值说明
```
code 请参考状态码
updateTime 当前API的最近更新时间
fxLink 当前数据的响应式页面，便于嵌入网站或应用
now.obsTime 数据观测时间
now.temp 温度，默认单位：摄氏度
now.feelsLike 体感温度，默认单位：摄氏度
now.icon 天气状况的图标代码，另请参考天气图标项目
now.text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
now.wind360 风向360角度
now.windDir 风向
now.windScale 风力等级
now.windSpeed 风速，公里/小时
now.humidity 相对湿度，百分比数值
now.precip 过去1小时降水量，默认单位：毫米
now.pressure 大气压强，默认单位：百帕
now.vis 能见度，默认单位：公里
now.cloud 云量，百分比数值。可能为空
now.dew 露点温度。可能为空
refer.sources 原始数据来源，或数据源说明，可能为空
refer.license 数据许可或版权声明，可能为空
```