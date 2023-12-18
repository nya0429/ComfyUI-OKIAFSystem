import time
import json
from urllib import request,error
import pprint
from datetime import datetime

api = "http://127.0.0.1:8188/prompt"
prompt_workflow = json.load(open('./workflow/workflow_api.json'))
pprint.pprint(prompt_workflow)

current_time = datetime.now().time()
start_time = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
end_time = current_time.replace(hour=22, minute=0, second=0, microsecond=0)

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

def get_queue_remaining():
    try:
        with request.urlopen(api) as response:
            content = response.read()
            data = json.loads(content)
            queue_remaining = data['exec_info']['queue_remaining']
            return queue_remaining
    except error.URLError as e:
        print("URLエラー:", e.reason)
        return 1
try:
    while True:
        if start_time <= datetime.now().time() <= end_time:
            queue_remaining = get_queue_remaining()
            if queue_remaining == 0:
                print("queue prompt")
                queue_prompt(prompt_workflow)
            time.sleep(1)
        else:
            time.sleep(30)
            print("sleep")
except KeyboardInterrupt:
    print("exit auto queue")