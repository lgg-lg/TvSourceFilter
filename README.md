# TvSourceFilter

## 电视源抓取及清理项目
### 文件说明
#### config文件夹
blacklist:源网址中包含字符串黑名单文件，#开头行为注释
whitelist: 源网址中包含字符串白名单文件，#开头行为注释
channels: 周一三五日上午自动运行会按此文件中单行抓取频道源，#开头行为注释
localsource：可自定义一些用户用过的频道源，用于总源收集，#开头行为注释
user_result：类同于localsource.txt，用于总源收集，#开头行为注释
othernames：设置处理频道别名，每个想获取的频道都建议做一个别名，#开头行为注释
subscribe: 其他来源网络源路径配置，#开头行为注释
user_demo：用户想配置的直播源文件样板
#### output文件夹
allsource: 源网址总集-自动生成
allsourcecleaned: 根据黑名单筛选后的源网址总集-自动生成
netsource：根据配置的subscribe文件自动合成源网址总集
ownsource：根据配置的channels文件自动抓取源网址总集
new_result：根据user_demo自动从channels各picked文件来生成的自定义直播源
channels文件夹：根据othernames处理的各频道源，_picked为白名单筛选
