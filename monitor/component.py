from .utils import import_from_string
from .worker import WorkerThread
import shortuuid

class Component():
  def __init__(self, name, assertions):
    self.name = name
    self.assertions = assertions

  def start(self):
    """
    Start threads for all assertions declared for a given component.
    """
    for assertion in self.assertions:
      AssertionClass = import_from_string(assertion["assertion"])
      kwargs = assertion.get("kwargs", {})
      settings = assertion.get("settings", {})

      assertion_object = AssertionClass(**kwargs)
      assertion_object.set_component_name(self.name)

      name = settings.get("name", shortuuid.uuid())
      assertion_object.set_friendly_name(name)

      thread = WorkerThread(assertion_object, interval=settings.get("interval", 1*60))
      thread.start()
