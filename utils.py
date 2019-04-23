import json

def get_defaults(key):
    with open("app_config.json") as f:
        data=json.loads(f.read())
        if key in data:
            return data[key]
        else:
            return None

def log_msg(msg):
    isDebug=get_defaults("mode")
    if isDebug=="Debug":
        print(msg)