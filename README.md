# Pocket48_toast
----
###### 仿口袋直播特效的ASS字幕转换器及一个下载lrc的小工具
---
这里有两个小工具，按说功能不同，该用新的仓库。
按说可以整合到一个里面，但最终还是一懒毁一切。
#### 已知缺陷：
1. 弹幕用户名与内容间存在阴影:
     - ASS字幕机理，有改动方案，但文件大小将成倍增加。暂不处理。
2. 字符显示不全
     - 聚聚们用的字符样式之多，还带表情。一般编码玩不过来，告辞告辞。
3. 原lrc字幕最后5位发言不予转换
     - 一般弹幕最后时间点会超出视频长度。即使转换，也不会显示。
4. 配色丑
     - 审美差，欢迎提供配色方案。
5. 代码写烂
     - 初学者，望斧正。


样例：     
![image](https://github.com/GNZ48live/Pocket48_to_ass/blob/master/Simple.jpg "蕾蕾镇楼")

------------
#### Usage for PtoA：
```
python PtoA.py ***.lrc (Your file）
```
```
新增可调参数
font_size：字体大小
line_spacing：行间距
line_num：显示行数
default_y_axis：整体弹幕高度（一般不需更改）
```
#### Usage for lrc_down:
```
按Read 按钮可以读取最新录播列表，按多一次翻下一页。
点选希望下载的后，点下方Download按钮，将下载致同目录下，以liveid命名的lrc文件。
```
