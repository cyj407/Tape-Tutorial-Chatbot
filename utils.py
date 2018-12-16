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
def send_image_url(id, image_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, os.environ.get("ACCESS_TOKEN"))
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "image", 
                "payload": {"url": image_url}
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send image: " + response.text)
    return response

# 送按鈕
def send_button_message(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, os.environ.get("ACCESS_TOKEN"))
    payload = {
        "recipient":{"id": id},
        "message":{
            "text": "請選擇要貼紮的部位：",
            "quick_replies":[
            {
                "content_type": "text",
                "payload": 5,
                "title": "xx肌肉"
            },
            {
                "content_type": "text",
                "payload": 5,
                "title": "xx肌肉"
            },
            {
                "content_type": "text",
                "payload": 5,
                "title": "xx肌肉"
            }]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send image: " + response.text)
    return response