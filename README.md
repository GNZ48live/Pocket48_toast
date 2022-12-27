# Pocket48_toast

----

###### 仿口袋直播特效的ASS字幕转换器及一个下载lrc的小工具

---

这里有两个小工具，按说功能不同，该用新的仓库。
按说可以整合到一个里面，但最终还是一懒毁一切。

#### 已知缺陷：
1. 字符显示不全
   - 聚聚们用的字符样式之多，以及所在机器的字体库也相关。
2. 原lrc字幕最后5位发言不予转换
   - 一般弹幕最后时间点会超出视频长度。即使转换，也不会显示。
3. 配色丑
   - 审美差，欢迎提供配色方案。
4. 代码写烂
   - 初学者，望斧正。

样例：     
<img src="https://github.com/GNZ48live/Pocket48_to_ass/blob/master/Simple.jpg" width = "300" alt="刘媛镇楼" />

------------

#### Usage for PtoA_gui_：

```
新增可调参数
font_size：字体大小
line_spacing：行间距
line_num：显示行数
default_y_axis：整体弹幕高度（一般不需更改）
default_x_axis：整体弹幕距左侧距离（因为有压制前后位置不一情况，可按需更改）
显示聚聚用户名选项框：勾选即显示

```

#### Usage for lrc_down:

```
按Read 按钮可以读取最新录播列表，按多一次翻下一页。
点选希望下载的后，点下方Download按钮，将下载致同目录下，以liveid命名的lrc文件。
M3u8 url显示录播地址，可选择M3u8支持的软件下载。
```
