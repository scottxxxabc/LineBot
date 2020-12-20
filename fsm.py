from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_starburst(self, event):
        text = event.message.text
        flag = False
        starburst_list = ["starburst", "星爆", "猩抱", "星爆氣流斬", "星光連流擊", "10 16", "星光流連擊", "撐10秒", "撐十秒", "十秒十六連擊"/
                        , "10秒十六連擊", "十秒16連擊", "雜燴兔", "艾恩葛朗特", "桐人", "桐谷", "騙人的吧", "閃耀魔眼", "封弊", "刀劍"/
                        , "雙刀", "雙劍", "闡釋者", "逐暗者", "等級制mmo的不合理之處", "74層", "8763", "還要更快", "第二把", "切換", "sao"/
                        , "2022", "夜空之劍", "藍薔薇", "就憑你這菜b8，笑死", "nervgear", "微笑棺木", "晶彥", "希茲克利夫", "嗨呀庫", "川原礫"/
                        , "我不能說", "切換", "化成", "潛行者" , "獨行", "兩把刀"]

        if (text.lower().find('10') or text.lower().find('十')) and (text.lower().find('16') or text.lower().find('十六')):
            flag = True
            return flag
        if (text.lower().find('blue') or text.lower().find('藍')) and (text.lower().find('black') or text.lower().find('黑')):
            flag = True
            return flag
        if text.lower().find('化成') and text.lower().find('我都認得'):
            flag = True
            return flag
        if text.lower().find('sword') and text.lower().find('art'):
            flag = True
            return flag
        for word in starburst_list:
            if text.lower().find(word)
                flag = True
                break   
            

        return flag

    def is_going_to_meme(self, event):
        text = event.message.text
        return text.lower() == "go to meme"

    def on_enter_starburst(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
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
