from . import BaseAssertion

try:
  import requests
except:
  raise ImportError("Http assertions require the 'requests' module to be intalled")

class ResourceStatusCode(BaseAssertion):
  def __init__(self, url, expected_status_code):
    self.url = url
    self.expected_status_code = expected_status_code
    super(ResourceStatusCode, self).__init__()

  def test(self):
    request = requests.get(self.url)

    if request.status_code != self.expected_status_code:
      self.raise_partial_outage()
