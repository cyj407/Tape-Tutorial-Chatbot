from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "test"
machine = TocMachine(
    states=[
        'start',
        'arm',
        'body',
        'leg',
        'arm_muscle',
        'body_muscle',
        'leg_muscle',
        'finish',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'arm',
            'conditions': 'arm_taping_first'
        },
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'body',
            'conditions': 'body_taping_first'
        },
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'leg',
            'conditions': 'leg_taping_first'
        },
        {   # arm
            'trigger': 'advance',
            'source': 'arm',
            'dest': 'arm_muscle',     
            'conditions': 'arm_taping_second'
        },
        {   # body
            'trigger': 'advance',
            'source': 'body',
            'dest': 'body_muscle',
            'conditions': 'body_taping_second'
        },
        {   # leg
            'trigger': 'advance',
            'source': 'leg',
            'dest': 'leg_muscle',
            'conditions': 'leg_taping_second'
        },
        {
            'trigger': 'advance',
            'source': [
                'arm_muscle',
                'body_muscle',
                'leg_muscle'
            ],
            'dest': 'finish',
            'conditions': 'watch_video'
        },
        {
            'trigger': 'advance',
            'source': [
                'arm_muscle',
                'body_muscle',
                'leg_muscle'
            ],
            'dest': 'start',
            'conditions': 'watch_other_video'
        },
        {
            'trigger': 'advance',
            'source': 'finish',
            'dest': 'start',
            'conditions': 'response'
        },
    ],
    initial='start',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if(event):
            machine.advance(event)
        return 'OK'

# 顯示圖
@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
