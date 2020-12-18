from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog
import os
import re
import textwrap
import sys


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.label1 = Label(self,text='Lrc 文件：')
        self.nameInput1 = Entry(self,width=25)
        self.alertButton1 = Button(self, text='打开', command=self.filepath_fetch)
        self.label2 = Label(self,text='字体大小：')
        self.nameInput2 = Entry(self,width=5)
        self.label3 = Label(self,text='行间距：')
        self.nameInput3 = Entry(self,width=5)
        self.label4 = Label(self,text='显示行数：')
        self.nameInput4 = Entry(self,width=5)
        self.label5 = Label(self,text='弹幕起始：')
        self.nameInput5 = Entry(self,width=5)
        self.alertButton2 = Button(self, text='转换', command=self.to_ass,width=10)
        
        self.label1.grid(row=0,column=0,padx=3)
        self.nameInput1.grid(row=0,column=1,padx=1)
        self.alertButton1.grid(row=0,column=2,padx=3)
        self.label2.grid(row=0,column=3)
        self.nameInput2.grid(row=0,column=4)
        self.label3.grid(row=1,column=3)
        self.nameInput3.grid(row=1,column=4)
        self.label4.grid(row=2,column=3)
        self.nameInput4.grid(row=2,column=4)
        self.label5.grid(row=3,column=3)
        self.nameInput5.grid(row=3,column=4)
        self.alertButton2.grid(row=2,column=0)

        self.nameInput2.insert(0, 20)
        self.nameInput3.insert(0, 38)
        self.nameInput4.insert(0, 6)
        self.nameInput5.insert(0, 790)

    def filepath_fetch(self):
        self.nameInput1.delete(0,'end')
        file_path = tkinter.filedialog.askopenfilename()
        self.nameInput1.insert(0,file_path)

    def to_ass(self):
        timestamps = []
        user = []
        info = []
        #Setting
        try:
            font_size = int(self.nameInput2.get())        #font_size = 20
            line_spacing = int(self.nameInput3.get())   #line_spacing = 38
            line_num = int(self.nameInput4.get())        #line_num = 6
            default_y_axis = int(self.nameInput5.get())  #default_y_axis = 790
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
        Style: Default,微软雅黑,{font_size},&H00F0F0F0,&H00FFFFFF,&H4C533B3B,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,2.5,1,20,275,27,1
        Style: D2,微软雅黑,{font_size},&H00FFCF9C,&H00FFFFFF,&H4C533B3B,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,2.5,1,74,275,27,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        '''
        #Path input
        lrc_path = self.nameInput1.get()
        if not lrc_path:
            messagebox.showinfo('Remind', '请输入Lrc文件')
            return
        file_name = lrc_path.replace('.lrc','.ass')
        if os.path.exists(file_name) == True:
            if messagebox.askokcancel('Caution','文件已存在，是否覆盖') == False:
                return
        with open(lrc_path,encoding='utf-8') as fin:
            with open(f'{file_name}','w',encoding='utf-8') as fout:
                i = 1
                #用户与信息分离
                for line in fin:
                    try:
                        line = re.split(r']|\t',line)
                        line_time = line[0]
                        timestamps.append(line_time[1:-1]) 
                        user.append(line[1])
                        info.append(' ' + line[2].replace('\n',''))
                        i += 1
                    except:
                        error_logging = f'第{i}行 内容： {line} 错误'
                        i += 1
                        pass
        #ASS Header Writing
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
                            Dialogue = f'Dialogue: 4,{time_star},{time_end},Default,,0,0,0,,{{\pos(20,{y_axis})}}{{{t}D2}}{user_}:{{{t}}}{info_}'
                            fout.write(Dialogue + '\n')           
                    b += 1
        self.nameInput1.delete(0,'end')
        messagebox.showinfo('Completed', '转换成功')

app = Application()
# 设置窗口标题:
app.master.title('Pocket48 lrc to ass')
app.master.geometry('500x120')
# 主消息循环:
app.mainloop()