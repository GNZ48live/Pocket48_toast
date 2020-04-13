import os
import re
import textwrap
import sys
import argparse

timestamps = []
user = []
info = []
y_axis_list = [790,753,716,679,642]
Def_info = textwrap.dedent('''
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
Style: Default,微软雅黑,15,&H00F0F0F0,&H00FFFFFF,&H4C533B3B,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,2.5,1,20,275,27,1
Style: D2,微软雅黑,15,&H00FFCF9C,&H00FFFFFF,&H4C533B3B,&H910E0807,0,0,0,0,100.0,100.0,0.0,0.0,3,6.1923075,2.5,1,74,275,27,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
''')
def main():
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('lrc_file')
    args = parser.parse_args()
    fin = args.lrc_file
    
    file_name = args.lrc_file.split('.')
    file_name = file_name[0]

    with open(args.lrc_file,encoding='utf-8') as fin:
        with open(f'{file_name}.ass','w',encoding='utf-8') as fout:
            for line in fin:
                line = re.split(r']|\t',line)
                line_time = line[0].replace('[','')
                timestamps.append(line_time[1:-1])
                user.append(line[1])
                info.append(' ' + line[2].replace('\n',''))      
        #ASS Header Writing
            fout.write(Def_info)

            t = '\\r'
            b = 1
            for user_,info_ in zip(user,info):
                for n,y_axis in zip(range(1,6),y_axis_list):
                    time_start_num = n + b - 2
                    time_end_num = n + b - 1
                    try:
                        time_star = timestamps[time_start_num]
                        time_end = timestamps[time_end_num]
                    except BaseException:
                        break
                    else:
                        Dialogue = f'Dialogue: 4,{time_star},{time_end},Default,,0,0,0,,{{\pos(20,{y_axis})}}{{{t}D2}}{user_}:{{{t}}}{info_}'
                        fout.write(Dialogue + '\n')
                
                b += 1

if __name__ == '__main__':
    main()
