from tkinter import *
from ttkbootstrap import *
from tkinter.ttk import *
from typing import Dict
import requests
import json
import time
import sys
from tkinter import messagebox
from tkinter import filedialog
import os
import re

class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_file_path"] = self.__tk_label_file_path(self)
        self.widget_dic["tk_text_path"] = self.__tk_text_path(self)
        self.widget_dic["tk_button_load"] = self.__tk_button_load(self)
        self.widget_dic["tk_button_trans"] = self.__tk_button_trans(self)
        self.widget_dic["tk_check_button_transs"] = self.__tk_check_button_transs(self)
        self.widget_dic["tk_label_size"] = self.__tk_label_size(self)
        self.widget_dic["tk_input_size"] = self.__tk_input_size(self)
        self.widget_dic["tk_label_spacing"] = self.__tk_label_spacing(self)
        self.widget_dic["tk_input_spacing"] = self.__tk_input_spacing(self)
        self.widget_dic["tk_label_lines"] = self.__tk_label_lines(self)
        self.widget_dic["tk_input_lines"] = self.__tk_input_lines(self)
        self.widget_dic["tk_label_X"] = self.__tk_label_X(self)
        self.widget_dic["tk_input_X"] = self.__tk_input_X(self)
        self.widget_dic["tk_label_Y"] = self.__tk_label_Y(self)
        self.widget_dic["tk_input_Y"] = self.__tk_input_Y(self)

        self.widget_dic["tk_input_size"].insert(0, 20)
        self.widget_dic["tk_input_spacing"].insert(0, 35)
        self.widget_dic["tk_input_lines"].insert(0, 6)
        self.widget_dic["tk_input_X"].insert(0, 20)
        self.widget_dic["tk_input_Y"].insert(0, 800)

    def __win(self):
        self.title("PtoA")
        # 设置窗口大小、居中
        width = 571
        height = 205
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    
    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)

    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)
        
    def __tk_label_file_path(self,parent):
        label = Label(parent,text="文件：",anchor="center", )
        label.place(x=30, y=30, width=50, height=30)
        return label

    def __tk_text_path(self,parent):
        text = Text(parent)
        text.place(x=90, y=30, width=369, height=30)
        return text

    def __tk_button_load(self,parent):
        btn = Button(parent, text="加载", takefocus=False,)
        btn.place(x=479, y=27, width=73, height=33)
        return btn

    def __tk_button_trans(self,parent):
        btn = Button(parent, text="转换", takefocus=False,)
        btn.place(x=480, y=150, width=73, height=33)
        return btn

    def __tk_check_button_transs(self,parent):
        self.var = IntVar()
        cb = Checkbutton(parent,text="显示用户名",variable=self.var,bootstyle="round-toggle")
        cb.place(x=370, y=153, width=90, height=30)
        return cb

    def __tk_label_size(self,parent):
        label = Label(parent,text="字体大小:",anchor="center", )
        label.place(x=22, y=90, width=57, height=30)
        return label

    def __tk_input_size(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=90, width=36, height=30)
        return ipt

    def __tk_label_spacing(self,parent):
        label = Label(parent,text="行间距:",anchor="center", )
        label.place(x=135, y=90, width=50, height=30)
        return label

    def __tk_input_spacing(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=181, y=90, width=36, height=30)
        return ipt

    def __tk_label_lines(self,parent):
        label = Label(parent,text="显示行数:",anchor="center", )
        label.place(x=230, y=90, width=58, height=30)
        return label

    def __tk_input_lines(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=290, y=90, width=36, height=30)
        return ipt

    def __tk_label_X(self,parent):
        label = Label(parent,text="起始X轴:",anchor="center", )
        label.place(x=340, y=90, width=50, height=30)
        return label

    def __tk_input_X(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=390, y=90, width=36, height=30)
        return ipt

    def __tk_label_Y(self,parent):
        label = Label(parent,text="起始Y轴:",anchor="center", )
        label.place(x=440, y=90, width=50, height=30)
        return label

    def __tk_input_Y(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=490, y=90, width=36, height=30)
        return ipt

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def time_transfer(self,timestamp):
        time_ = time.localtime(int(timestamp)/1000)
        format_time = time.strftime("%Y-%m-%d %H:%M:%S",time_)
        return format_time

    def to_ass(self,evt):
        timestamps = []
        user = []
        info = []
        try:
            font_size = int(self.widget_dic["tk_input_size"].get())        #font_size = 20
            line_spacing = int(self.widget_dic["tk_input_spacing"].get())   #line_spacing = 35
            line_num = int(self.widget_dic["tk_input_lines"].get())        #line_num = 6
            default_y_axis = int(self.widget_dic["tk_input_Y"].get())  #default_y_axis = 800
            x_axis = int(self.widget_dic["tk_input_X"].get())  #default_y_axis = 20
        except:
            return messagebox.showinfo('Caution!', '请确保参数正确')

        y_axis_list = [default_y_axis-spacing*line_spacing for spacing in range(line_num)]
        Def_info = f'''
[Script Info]
Title: Default ASS file
ScriptType: v4.00+
WrapStyle: 2
Collisions: Normal
PlayResX: 384
PlayResY: 816
ScaledBorderAndShadow: yes
Video Zoom Percent: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,{font_size},&H00F6FCFF,&H00FFFFFF,&H88000000,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,0,1,20,275,27,1
Style: D2,微软雅黑,{font_size},&H00F6FCFF,&H00FFFFFF,&H88000000,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,0,1,74,275,27,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        #Path input
        lrc_path = self.widget_dic["tk_text_path"].get(1.0,END)
        if not lrc_path:
            messagebox.showinfo('Remind', '请输入Lrc文件')
            return
        file_name = lrc_path.replace('.lrc','.ass')
        if os.path.isfile(file_name.strip()) == True:
            if messagebox.askyesno('Caution','文件已存在，是否覆盖') == False:
                return
        with open(lrc_path.strip(),encoding='utf-8') as fin:
            with open(file_name.strip(),'w',encoding='utf-8') as fout:
                i = 1
                #用户与信息分离
                for line in fin:
                    try:
                        if ']' in line:
                            line = re.split(']|\t',line)
                            line_time = line[0]
                            timestamps.append(line_time[1:])
                            user.append(line[1])
                            info.append(' ' + line[2].replace('\n',''))
                            i += 1
                    except:
                        #print(f'第{i}行 内容： {line} 错误')
                        i += 1
                        pass
        #ASS Header                    
                fout.write(Def_info)
       
                t = '\\r'
                b = 1
                for user_,info_ in zip(user,info):
                    for n,y_axis in zip(range(1,line_num+1),y_axis_list):
                        time_start_num = n + b - 2
                        time_end_num = n + b - 1
                        try:
                            time_star = timestamps[time_start_num]
                            time_end = timestamps[time_end_num]
                        except:
                            pass
                        else:
                            var = IntVar()
                            if n != 1:                            
                                if self.var.get() == 0:
                                    Dialogue = f'Dialogue: 4,{time_star},{time_end},Default,,0,0,0,,{{\pos({x_axis},{y_axis})}}{info_}'
                                    fout.write(Dialogue + '\n')
                                else:
                                    Dialogue = f'Dialogue: 4,{time_star},{time_end},Default,,0,0,0,,{{\pos({x_axis},{y_axis})}}{{{t}D2}}{user_}:{info_}'
                                    fout.write(Dialogue + '\n')
                            else:
                                Dialogue = f'Dialogue: 4,{time_star},{time_end},Default,,0,0,0,,{{\pos({x_axis},{y_axis})}}{{\\fad(400,80)}}{info_}'
                                fout.write(Dialogue + '\n')

                    b += 1
        self.widget_dic["tk_text_path"].delete(1.0,END)
        messagebox.showinfo('Completed', '转换成功')

    def time_adjust(self,evt):
        if self.widget_dic["tk_text_path"].get(1.0,END):
            lrc_path = self.widget_dic["tk_text_path"].get(1.0,END)
        else:
            messagebox.showinfo('Caution','请加载字幕文件')
        file_name = lrc_path[0:-4] + '_adjuested' + '.lrc'
        timestamp_n = []
        if self.widget_dic["tk_input_second"].get():
            second = int(self.widget_dic["tk_input_second"].get())
        else:
            messagebox.showinfo('Caution','请输入秒数')
        with open(lrc_path.strip(),encoding='utf-8') as fin:
            with open(file_name.strip(),'w',encoding='utf-8') as fout:
                for line in fin:
                    timestamp_tem = re.findall('\[([0-9]{0,2}\:[0-9]{0,2}\:[0-9]{0,2}\.[0-9]{0,3})\]',line)
                    line = re.split(r']|\t',line)
                    timestamp = timestamp_tem[0]
                    second_n = int(timestamp[3:5]) * 60 + int(timestamp[6:8]) + second
                    if second_n < 0:
                        second_n = 0
                    min_n = second_n // 60
                    second_n = '{:02d}'.format(second_n % 60)
                    timestamp = f'{timestamp[0:3]}{str(min_n)}:{str(second_n)}{timestamp[8:]}'
                    line2 = line[2]
                    new_line = f'[{timestamp}]{line[1]}\t{line2}'           
                    fout.write(new_line)
                messagebox.showinfo('Completed', '调整成功')

    def filepath_fetch(self,evt):
        self.widget_dic["tk_text_path"].delete(1.0,END)
        file_path = filedialog.askopenfilename()
        self.widget_dic["tk_text_path"].insert(1.0,file_path)

    def __event_bind(self):
        self.widget_dic["tk_button_load"].bind('<Button-1>',self.filepath_fetch)
        self.widget_dic["tk_button_trans"].bind('<Button-1>',self.to_ass)
        pass
        
if __name__ == "__main__":
    win = Win()
    win.mainloop()
