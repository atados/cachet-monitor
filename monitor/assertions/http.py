from . import BaseAssertion

try:
  import requests
except:
  raise ImportError("Http assertions require the 'requests' module to be installed")

class ResourceStatusCode(BaseAssertion):
  def __init__(self, url, expected_status_code):
    self.url = url
    self.expected_status_code = expected_status_code
    super(ResourceStatusCode, self).__init__()

  def test(self):
    try:
      request = requests.get(self.url)
    except:
      self.raise_failure()

    if request.status_code != self.expected_status_code:
      self.raise_failure()
