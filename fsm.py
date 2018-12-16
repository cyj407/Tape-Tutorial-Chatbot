from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_image_url
from utils import send_button_message

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def arm_taping_first(self, event):
        print("in arm_taping_first")
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'arm'
        return False

    def arm_taping_second(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'arm_2'
        return False

    def arm_taping_third(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'arm_3'
        return False

    def arm_taping_final(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'arm_4'
        return False

    def on_enter_arm(self, event):
        output = "I'm entering arm"
        print(output)
        sender_id = event['sender']['id']
        img_url = "https://i.imgur.com/fTj1ubb.jpg"
        responese = send_image_url(sender_id, img_url)
        responese = send_button_message(sender_id)
