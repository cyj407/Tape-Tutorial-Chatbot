from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def arm_taping_first(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'arm'
        return False

    def body_taping_first(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'body'
        return False
    
    def leg_taping_first(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'leg'
        return False

    def on_enter_arm(self, event):
        output = "I'm entering arm"
        print(output)

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, output)
        # self.go_back()

    def on_enter_body(self, event):
        output = "I'm entering body"
        print(output)

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, output)

    def on_enter_leg(self, event):
        output = "I'm entering leg"
        print(output)

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, output)

    '''
    def on_exit_state1(self):
        print('Leaving state1')
    '''


    '''
    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "I'm entering state2")
        self.go_back()

    def on_exit_state2(self):
        print('Leaving state2')
    '''
