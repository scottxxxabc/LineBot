from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url, send_button_message
import os

from linebot.models import PostbackEvent



class TocMachine(GraphMachine):
    starburst_list = []
    starburst_img = []
    starburst_article = []
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        with open("starburstword.txt",'r', encoding='UTF-8') as f:
            for word in f:
                self.starburst_list.append(word.replace('\n', ''))
        with open("img_url.txt",'r', encoding='UTF-8') as f:
            for word in f:
                self.starburst_img.append(word.replace('\n', ''))
        allFileList = os.listdir('./article')
        for file in allFileList:
            if os.path.isfile('./article/' + file):
                self.starburst_article.append(file)

    def test(self, event):

        if self.state == "user":
            self.advance(event)
        elif self.state == "starburstpolice":
            if event.message.text.lower() == "exit":
                send_text_message(event.source.user_id, "您已離開星爆文字獄")
                self.check_end(event)
            else:
                self.check(event)
        elif self.state == "wordmanage":
            text = event.message.text
            if text.lower() == 'exit':
                with open("starburstword.txt",'w', encoding='UTF-8') as f:
                    for word in self.starburst_list:
                        f.write(word + '\n')
                send_text_message(event.source.user_id, "您已結束星爆關鍵字管理")
                self.manage_end(event)
                return
            str = (text.split('\n', 1))[0].split(' ', 1)

            if str[0].lower() == 'add' and len(str) > 1:
                if str[1] != '':
                    self.add_to_list(str[1], event)
                    return
            elif str[0].lower() == 'rm' and len(str) > 1:
                self.rm(str[1], event)
                return
            elif str[0].lower() == 'list':
                self.list(event)
                return
            elif str[0].lower() == 'search' and len(str) > 1:
                self.search(str[1], event)
                return
            
            send_text_message(event.source.user_id, text + ' 不是正確的指令')

        elif self.state == "meme":
            text = event.message.text
            if isinstance(event, PostbackEvent):
                if event.postback.data == 'YES':
                    send_button_message(event.source.user_id, self.starburst_img)
                elif event.postback.data == 'NO':
                    send_text_message(event.source.user_id, '我對你感到很失望')
                return
            elif text.lower() == 'exit':
                self.go_back()
                return
            elif text.lower() == '0':
                send_button_message(event.source.user_id, self.starburst_img)
                return
            elif int(text.lower())>=1 and int(text.lower())<=len(self.starburst_article):
                with open(self.starburst_article[int(text.lower())-1],'r', encoding='UTF-8') as f:
                    send_text_message(event.source.user_id, f.read())



    def add_to_list(self, str, event):
        if str in self.starburst_list:
            send_text_message(event.source.user_id, str + ' 已在星爆關鍵字列表中!')

        else:
            self.starburst_list.append(str)
            with open("starburstword.txt",'a', encoding='UTF-8') as f:
                f.write(str + '\n')
            send_text_message(event.source.user_id, str + ' 已加入星爆關鍵字列表!')



    def rm(self, str, event):
        if str in self.starburst_list:
            if str != '':
                self.starburst_list.remove(str)
                send_text_message(event.source.user_id, str + ' 已從星爆關鍵字列表移除!')
                
        else:
            send_text_message(event.source.user_id, str + ' 不在星爆關鍵字列表中!')

    def list(self, event):
        str = ''
        for word in self.starburst_list:
            str = str + word + '\n'
        send_text_message(event.source.user_id, str)

    def search(self, str, event):
        if str in self.starburst_list:
            send_text_message(event.source.user_id, str + ' 已在星爆關鍵字列表中!')
        else:
            send_text_message(event.source.user_id, str + ' 不在星爆關鍵字列表中!')


    def is_going_to_help(self, event):
        text = event.message.text
        return text.lower() == "help"

    def on_enter_help(self, event):
        help_message = "歡迎使用星爆大師~\n這是一個可以幫助你找出正在偷星爆的星爆仔的好東西~\n\n輸入 0 以開始你的思想審查\n輸入 1 管理星爆關鍵字\n輸入 2 觀賞星爆迷因"
        id = event.source.user_id
        send_text_message(id, help_message)
        self.go_back()

    def is_going_to_starburstpolice(self, event):
        text = event.message.text
        if  text.lower() == "0": 
            send_text_message(event.source.user_id, "進入星爆警察模式\n請輸入您想審查的文字開始您的星爆文字獄\n輸入 exit 結束審查")
            self.starburst_list.clear()
            with open("starburstword.txt",'r', encoding='UTF-8') as f:
                for word in f:
                    self.starburst_list.append(word.replace('\n', ''))
            return True
        else:
            return False



    def is_going_to_starburst(self, event):
        text = event.message.text
        flag = False
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
        for word in self.starburst_list:
            if text.lower().find(word)!=-1:
                flag = True
                break   
        if flag == False:
            id = event.source.user_id
            send_text_message(id, "沒有偷偷星爆，很棒喔")
        
        return flag

    def on_enter_starburst(self, event):
        print("I'm entering state1")

        id = event.source.user_id
        send_text_message(id, "化成\n" + event.message.text + "\n我都認得")
        send_text_message(id, "吃噓")
        send_image_url(id, 'https://imgur.com/eYnSVP8.png')
        
        self.starburst_end()


    def is_going_to_meme(self, event):
        text = event.message.text
        return text.lower() == "2"

    def on_enter_meme(self, event):

        id = event.source.user_id
        stri = '您現在可以觀賞最棒的星爆圖及星爆文!\n\n輸入 0 觀賞星爆圖'
        for index, a in enumerate(self.starburst_article) :
            stri = stri + '\n輸入' + str(index + 1) + " " + a[:a.find('.')]
        stri = stri + "\n輸入 exit 離開"
        send_text_message(id, stri)

    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_fsm(self, event):

        id = event.source.user_id
        send_text_message(id, "fsm")
        self.go_back() 


    def is_going_to_wordmanage(self, event):
        text = event.message.text
        return text.lower() == "1"

    def on_enter_wordmanage(self, event):
        id = event.source.user_id
        send_text_message(id, "您已進入管理星爆關鍵字\n\n輸入 add {關鍵字} 新增星爆關鍵字\n"+
                        "輸入 rm {關鍵字} 移除星爆關鍵字\n輸入 search {關鍵字} 查詢星爆關鍵字"+
                        "\n輸入 list 列出所有星爆關鍵字\n輸入 exit 離開")
