import requests
import os


GRAPH_URL = "https://graph.facebook.com/v2.6"

# 送文字訊息
def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, os.environ.get("ACCESS_TOKEN"))
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


# 送圖片
def send_image_url(id, img_url):
    pass

# 送按鈕
def send_button_message(id, text, buttons):
    pass
