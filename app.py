from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "test"
machine = TocMachine(
    states=[
        'user',
        'arm',
        'body',
        'leg',
        'ECUM',                   # 伸腕肌
        'FCUM',                   # 屈腕肌 
        'TRICEPS',                # 三頭肌
        'DELTOID',                # 三角肌
        'ILIOCOSTAL',             # 豎脊肌
        'QUADRICEPS',             # 股四頭肌
        'TIBIALIS',               # 脛前肌
        'GASTRO',                 # 腓腸肌
        'ECUM_FINAL',             # 伸腕肌
        'FCUM_FINAL',             # 屈腕肌 
        'TRICEPS_FINAL',          # 三頭肌
        'DELTOID_FINAL',          # 三角肌
        'ILIOCOSTAL_FINAL',       # 豎脊肌
        'QUADRICEPS_FINAL',       # 股四頭肌
        'TIBIALIS_FINAL',         # 脛前肌
        'GASTRO_FINAL',           # 腓腸肌
        'finish'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'arm',
            'conditions': 'arm_taping_first'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'body',
            'conditions': 'body_taping_first'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'leg',
            'conditions': 'leg_taping_first'
        },
        {   # arm
            'trigger': 'choose',
            'source': 'arm',
            'dest': 'ECUM',     
            'conditions': 'arm_taping_second'
        },
        {   # arm
            'trigger': 'choose',
            'source': 'arm',
            'dest': 'FCUM',     
            'conditions': 'arm_taping_second'
        },
        {   # arm
            'trigger': 'choose',
            'source': 'arm',
            'dest': 'TRICEPS',     
            'conditions': 'arm_taping_second'
        },
        {   # body
            'trigger': 'advance',
            'source': 'body',
            'dest': 'DELTOID',
            'conditions': 'body_taping_second'
        },
        {   # body
            'trigger': 'advance',
            'source': 'body',
            'dest': 'ILIOCOSTAL',
            'conditions': 'body_taping_second'
        },
        {   # leg
            'trigger': 'advance',
            'source': 'leg',
            'dest': 'QUADRICEPS',
            'conditions': 'leg_taping_second'
        },
        {   # leg
            'trigger': 'advance',
            'source': 'leg',
            'dest': 'TIBIALIS',
            'conditions': 'leg_taping_second'
        },
        {   # leg
            'trigger': 'advance',
            'source': 'leg',
            'dest': 'GASTRO',
            'conditions': 'leg_taping_second'
        },
        {   # arm_last
            'trigger': 'advance',
            'source': 'ECUM',
            'dest': 'ECUM_FINAL',     
            'conditions': 'arm_taping_third'
        },
        {   # arm_last
            'trigger': 'advance',
            'source': 'FCUM',
            'dest': 'FCUM_FINAL',     
            'conditions': 'arm_taping_third'
        },
        {   # arm_last
            'trigger': 'advance',
            'source': 'TRICEPS',
            'dest': 'TRICEPS_FINAL',     
            'conditions': 'arm_taping_third'
        },
        {   # body_last
            'trigger': 'advance',
            'source': 'DELTOID',
            'dest': 'DELTOID_FINAL',
            'conditions': 'body_taping_third'
        },
        {   # body_last
            'trigger': 'advance',
            'source': 'ILIOCOSTAL',
            'dest': 'ILIOCOSTAL_FINAL',
            'conditions': 'body_taping_third'
        },
        {   # leg_last
            'trigger': 'advance',
            'source': 'QUADRICEPS',
            'dest': 'QUADRICEPS_FINAL',
            'conditions': 'leg_taping_final'
        },
        {   # leg_last
            'trigger': 'advance',
            'source': 'TIBIALIS',
            'dest': 'TIBIALIS_FINAL',
            'conditions': 'leg_taping_final'
        },
        {   # leg_last
            'trigger': 'advance',
            'source': 'GASTRO',
            'dest': 'GASTRO_FINAL',
            'conditions': 'leg_taping_final'
        },
        {
            'trigger': 'advance',
            'source': [
                'ECUM_FINAL',             # 伸腕肌
                'FCUM_FINAL',             # 屈腕肌 
                'TRICEPS_FINAL',          # 三頭肌
                'DELTOID_FINAL',          # 三角肌
                'ILIOCOSTAL_FINAL',       # 豎脊肌
                'QUADRICEPS_FINAL',       # 股四頭肌
                'TIBIALIS_FINAL',         # 脛前肌
                'GASTRO_FINAL',           # 腓腸肌
            ],
            'dest': 'finish'
        },
        {
            'trigger': 'go_back',
            'source': 'finish',
            'dest': 'user'
        }
    ],
    initial='user',
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
        if(event and machine.state != "arm"):
            machine.advance(event)
        return 'OK'


# 顯示圖
@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
