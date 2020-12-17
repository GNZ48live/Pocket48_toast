import os
import re
import textwrap
import sys
import argparse


timestamps = []
user = []
info = []
#Setting

font_size = 20        #font_size = 20
line_spacing = 38     #line_spacing = 38
line_num = 6          #line_num = 6
default_y_axis = 780  #default_y_axis = 790

#ass字幕文件头及样式
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
def spacing_calculator():
    y_axis_list = [default_y_axis-spacing*line_spacing for spacing in range(line_num)]
    return y_axis_list
def main():
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('lrc_file')
    args = parser.parse_args()
    fin = args.lrc_file
    
    file_name = args.lrc_file.split('.')
    file_name = file_name[0]
    y_axis_list = spacing_calculator()

    with open(args.lrc_file,encoding='utf-8') as fin:
        with open(f'{file_name}.ass','w',encoding='utf-8') as fout:
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
                    print(error_logging)
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
                

if __name__ == '__main__':
    main()
