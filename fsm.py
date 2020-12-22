from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def test(self, event):
        if self.state == "user":
            return self.advance(event)

    def is_going_to_help(self, event):
        text = event.message.text
        return text.lower() == "help"

    def on_enter_help(self, event):
        print("I'm entering state2")
        help_message = "歡迎使用星爆大師~\n這是一個可以幫助你找出正在偷星爆的星爆仔的好東西~\n輸入 星爆警察 以開始你的思想審查\n"
        reply_token = event.reply_token
        send_text_message(reply_token, help_message)
        self.go_back()

    def is_going_to_starburst(self, event):
        text = event.message.text
        flag = False
        starburst_list = ["starburst", "星爆", "猩抱", "星爆氣流斬", "星光連流擊", "10 16", "星光流連擊", "撐10秒", "撐十秒", "十秒十六連擊"
                        , "10秒十六連擊", "十秒16連擊", "雜燴兔", "艾恩葛朗特", "桐人", "桐谷", "騙人的吧", "閃耀魔眼", "封弊", "刀劍"
                        , "雙刀", "雙劍", "闡釋者", "逐暗者", "等級制mmo的不合理之處", "74層", "8763", "還要更快", "第二把", "切換", "sao"
                        , "2022", "夜空之劍", "藍薔薇", "就憑你這菜b8，笑死", "nervgear", "微笑棺木", "晶彥", "希茲克利夫", "嗨呀庫", "川原礫"
                        , "我不能說", "切換", "化成", "潛行者" , "獨行", "兩把刀"]

        if (text.lower().find('10')!=-1 or text.lower().find('十')!=-1) \
            and (text.lower().find('16')!=-1 or text.lower().find('十六')!=-1):
            flag = True
            return flag
        if (text.lower().find('blue')!=-1 or text.lower().find('藍')!=-1) \
            and (text.lower().find('black')!=-1 or text.lower().find('黑')!=-1):
            flag = True
            return flag
        if text.lower().find('化成')!=-1 and text.lower().find('我都認得')!=-1:
            flag = True
            return flag
        if text.lower().find('sword')!=-1 and text.lower().find('art')!=-1:
            flag = True
            return flag
        for word in starburst_list:
            if text.lower().find(word)!=-1:
                flag = True
                break   
            
        
        return flag

    def is_going_to_meme(self, event):
        text = event.message.text
        return text.lower() == "go to meme"

    def on_enter_starburst(self, event):
        print("I'm entering state1")

        id = event.source.user_id
        send_text_message(id, "化成\n" + event.message.text + "\n我都認得")
        send_text_message(id, "吃噓")
        send_image_url(id, 'https://imgur.com/eYnSVP8.png')
        
        self.go_back()

    def on_exit_starburst(self):
        print("Leaving state1")

    def on_enter_meme(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "meme")
        self.go_back()

    def on_exit_meme(self):
        print("Leaving state2")
