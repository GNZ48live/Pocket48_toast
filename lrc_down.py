import tkinter as tk
import requests
import json
import time

app = tk.Tk() 
app.title('Pocket48_lrc')
app.geometry('600x300')
page_num = [0]
liveid = []
liveone_api = 'http://pocketapi.48.cn/live/api/v1/live/getLiveOne'
api_url = 'http://pocketapi.48.cn/live/api/v1/live/getLiveList'
headers = {
    'User-Agent': 'PocketFans201807/6.0.22_201211 (Pixel 2 XL:Android 10;Google scorpion_taimen-userdebug 10 QQ3A.200705.002 eng.gmathe.20200722.185025 release-keys)',
    'Content-Type': 'application/json;charset=UTF-8'
}
def time_transfer(timestamp):
    time_ = time.localtime(int(timestamp)/1000)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S",time_)
    return format_time

def fetch_data(page_num):
    lives_info = []
    button_next['text'] = 'Next'
    post_value = {"debug":'true',"next":page_num[0],"record":'true'}
    wbdata = requests.post(api_url,data=json.dumps(post_value),headers=headers).text
    raw_data = json.loads(wbdata)
    for info in raw_data['content']['liveList']:
        timestamp = info['ctime']
        live_time = time_transfer(timestamp)
        live_title = info['title']
        member = info['userInfo']['nickname']
        liveid_ = info['liveId']
        liveinfo_  = '-'.join([live_time,member,live_title])
        lives_info.append(liveinfo_)
        liveid.append(liveid_)
    main_listbox.delete(0,tk.END)
    for info_ in lives_info:
        main_listbox.insert(tk.END,info_)
    
    page_num[0] = int(raw_data['content']['next'])


def listbox_click(self):
    textbox.delete('1.0',tk.END)

    textbox.insert(tk.INSERT, liveid[main_listbox.index('anchor')])

def downloader():
    liveid_ = liveid[main_listbox.index('anchor')]
    post_value = {"liveId":liveid_}
    wbdata = requests.post(liveone_api,data=json.dumps(post_value),headers=headers).text
    live_info = json.loads(wbdata)
    lrc_url = live_info['content']['msgFilePath']
    m3u8_url = live_info['content']['playStreamPath']
    downloader = requests.get(lrc_url)
    with open(f'{liveid_}.lrc','wb') as fin:
        fin.write(downloader.content)
    textbox_url.delete('1.0',tk.END)
    textbox_url.insert(tk.INSERT,m3u8_url)

button_next = tk.Button(app,width=20,height=2,text='Read',command=lambda:fetch_data(page_num))
main_listbox = tk.Listbox(width=75,height=10)
label = tk.Label(text='LiveID:')
textbox = tk.Text(app,width=30,height=2)
scrollbar = tk.Scrollbar(app,command=main_listbox.yview)
main_listbox.configure(yscrollcommand=scrollbar.set)
button_download = tk.Button(app,width=20,height=2,text='Download',command=lambda:downloader())
label_url = tk.Label(text='M3U8 Url:')
textbox_url = tk.Text(app,width=30,height=2)

button_next.grid(row=0,column=2,columnspan=1,padx = 10,pady = 5,sticky = 'e')
label.grid(row=0,column=0,columnspan=1)
textbox.grid(row=0,column=1,columnspan=10,sticky = 'w')
main_listbox.grid(row=1,column=0,columnspan=3,sticky = 'ns',padx = 10)
scrollbar.grid(row=1,column=3,columnspan=1,sticky = 'ns')
button_download.grid(row=2,column=2,sticky = 'e',pady = 5)
label_url.grid(row=2,column=0,columnspan=1)
textbox_url.grid(row=2,column=1,columnspan=10,sticky = 'w')


main_listbox.bind('<<ListboxSelect>>', listbox_click)

app.mainloop()