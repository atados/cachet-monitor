import requests

class API():
  def __init__(self, url, token):
    self.url = url
    self.token = token

  def get_url(self, path):
    return "{}{}".format(self.url, path)

  def _get_headers(self):
    return {"X-Cachet-Token": self.token}

  def update_component(self, id, data):
    r = requests.put(self.get_url("/api/v1/components/{}".format(id)), json=data, headers=self._get_headers())

  def create_incident(self, id, data):
    data["component_id"] = id
    r = requests.post(self.get_url("/api/v1/incidents"), json=data, headers=self._get_headers())

  def component_has_open_incidents(self, id):
    r = requests.get(self.get_url("/api/v1/incidents?component_id={}&per_page=99999".format(id)))
    response = r.json()

    for incident in response["data"]:
      if incident["status"] != 4:
        return True

    return False
