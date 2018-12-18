from transitions.extensions import GraphMachine
from utils import send_text_message
from utils import send_image_url
from utils import send_button_message
from seg import seg_word
from scrape import getHotKey

class TocMachine(GraphMachine):
    muscle = []
    target = ""
    notFound = 0

    video_url = {
        "伸腕肌": "https://www.youtube.com/watch?v=t5FBuiUtT7c",
        "屈腕肌": "https://www.youtube.com/watch?v=s5IXNb3hGrs",
        "三頭肌": "https://www.youtube.com/watch?v=R0PMR-Ii25M",
        "三角肌": "https://www.youtube.com/watch?v=ijAUoeuztto",
        "豎脊肌": "https://www.youtube.com/watch?v=FYF7GSDtFG8",
        "股四頭肌": "https://www.youtube.com/watch?v=p3yfZNLijjU",
        "脛前肌": "https://www.youtube.com/watch?v=9bhgwv7c-kA",
        "腓腸肌": "https://www.youtube.com/watch?v=2bCT5LV1SBM",
    }


    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
    
    def no_advance_cond(self, event):
        print("in no_advance_cond")
        if(self.notFound >= 3):
            self.notFound = 0
            return True
        else:
            self.notFound = 0
            return False

    def arm_taping_first(self, event):
        print("in arm_taping_first")
        if event.get("message"):
            if('attachments' in event['message']):
                self.notFound = self.notFound + 1
                return False
            text = event['message']['text']
            seg_result = seg_word(text)
            for idx in seg_result:
                if(idx.find('手') != -1 or idx.find('腕') != -1 or
                 idx.find('肘') != -1 or idx.find('Shoulder') != -1):
                    return True
        self.notFound = self.notFound + 1
        return False

    def arm_taping_second(self, event):
        print("in arm_taping_second")
        if event.get("message"):
            text = event['message']['text']
            print(self.muscle)
            for idx in self.muscle:
                print(idx)
                if(text == idx):
                    return True
        return False

    def body_taping_first(self, event):
        print("in body_taping_first")
        if event.get("message"):
            if('attachments' in event['message']):
                self.notFound = self.notFound + 1
                return False
            text = event['message']['text']
            seg_result = seg_word(text)
            for idx in seg_result:
                if(idx.find('軀幹') != -1 or idx.find('腰') != -1 \
                or idx.find('背') != -1 or idx.find('肩') != -1):
                    return True
        self.notFound = self.notFound + 1
        return False

    def body_taping_second(self, event):
        print("in arm_taping_second")
        if event.get("message"):
            text = event['message']['text']
            print(self.muscle)
            for idx in self.muscle:
                print(idx)
                if(text == idx):
                    return True
        return False

    def leg_taping_first(self, event):
        print("in leg_taping_first")
        if event.get("message"):
            if('attachments' in event['message']):
                self.notFound = self.notFound + 1
                return False
            text = event['message']['text']
            seg_result = seg_word(text)
            for idx in seg_result:
                if(idx.find('腿') != -1 or idx.find('腳') != -1 or idx.find('足') != -1\
                or idx.find('膝') != -1 or idx.find('Knee') != -1):
                    return True
        self.notFound = self.notFound + 1
        return False

    def leg_taping_second(self, event):
        print("in leg_taping_second")
        if event.get("message"):
            text = event['message']['text']
            print(self.muscle)
            for idx in self.muscle:
                print(idx)
                if(text == idx):
                    return True
        return False

    def watch_video(self, event):
        print("in watch_video")
        if event.get("message"):
            text = event['message']['text']
            return text == '我要觀看'
        return False

    def watch_other_video(self, event):
        print("in watch_other_video")
        if event.get("message"):
            text = event['message']['text']
            return text == '選擇其他部位'
        return False

    def on_enter_arm(self, event):
        output = "I'm entering arm"
        print(output)
        sender_id = event['sender']['id']
        img_url = "https://i.imgur.com/ZVwD4uw.png"
        responese = send_image_url(sender_id, img_url)
        self.muscle = ["伸腕肌", "屈腕肌", "三頭肌"]
        text = "請選擇要貼紮的部位："
        responese = send_button_message(sender_id, text, self.muscle)

    def on_enter_arm_muscle(self, event):
        sender_id = event['sender']['id']
        self.target = event['message']['text']
        text = "是否要觀看" + self.target + "的貼紮教學影片？"
        option = ["我要觀看", "選擇其他部位"]
        responese = send_button_message(sender_id, text, option)

    def on_enter_body(self, event):
        output = "I'm entering body"
        print(output)
        sender_id = event['sender']['id']
        img_url = "https://i.imgur.com/ZIQxPqs.png"
        responese = send_image_url(sender_id, img_url)
        self.muscle = ["三角肌", "豎脊肌"]
        text = "請選擇要貼紮的部位："
        responese = send_button_message(sender_id, text, self.muscle)

    def on_enter_body_muscle(self, event):
        sender_id = event['sender']['id']
        self.target = event['message']['text']
        text = "是否要觀看" + self.target + "的貼紮教學影片？"
        option = ["我要觀看", "選擇其他部位"]
        responese = send_button_message(sender_id, text, option)

    def on_enter_leg(self, event):
        output = "I'm entering leg"
        print(output)
        sender_id = event['sender']['id']
        img_url = "https://i.imgur.com/NLuJRIw.png"
        responese = send_image_url(sender_id, img_url)
        self.muscle = ["股四頭肌", "脛前肌", "腓腸肌"]
        text = "請選擇要貼紮的部位："
        responese = send_button_message(sender_id, text, self.muscle)

    def on_enter_leg_muscle(self, event):
        sender_id = event['sender']['id']
        self.target = event['message']['text']
        text = "是否要觀看" + self.target + "的貼紮教學影片？"
        option = ["我要觀看", "選擇其他部位"]
        responese = send_button_message(sender_id, text, option)

    def on_enter_finish(self, event):
        sender_id = event['sender']['id']
        output = self.video_url[self.target]
        responese = send_text_message(sender_id, "以下是"+ self.target + "的教學影片：")
        responese = send_text_message(sender_id, output)
        responese = send_button_message(sender_id, "按下面按鈕以繼續", ["看其他影片"])

    def on_enter_start(self, event):
        print("return user")
        sender_id = event['sender']['id']
        responese = send_button_message(sender_id, "請描述你想要貼紮的部位~ 你可以考慮選擇熱門搜尋：", getHotKey())

    def response(self, event):
        print("in response")
        if event.get("message"):
            text = event['message']['text']
            return text != ''
        return False