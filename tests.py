import json
USER_LOG = "userLog.json"

with open(USER_LOG, 'r', encoding="utf-8") as file:
    data = json.load(file)


