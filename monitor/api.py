import requests

def get_headers():
  return {"X-Cachet-Token": "YqnyAjjntTCFLT8DRCpc"}

def update_component(id, data):
  r = requests.put("http://104.236.55.1/api/v1/components/{}".format(id), json=data, headers=get_headers())
