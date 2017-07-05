import threading
import time
import logging
import uuid

class WorkerThread(threading.Thread):
  def __init__(self, assertion, interval=1):
    super(WorkerThread, self).__init__()
    self.assertion = assertion
    self.interval = interval
    self.logger = logging.getLogger('monitor')

  def run(self):
    """
    Called when thread is started.
    """
    self.check_object()
    assertion_uuid = self.assertion.uuid
    component_name = self.assertion.component_name
    assertion_type = type(self.assertion).__name__

    i = 0
    while True:
      i += 1
      iteration_uuid = str(uuid.uuid4())
      self.logger.info("Running assertion {}/{}({}). Iteration: {}({})".format(component_name, assertion_type, assertion_uuid, i, iteration_uuid))
      self.assertion.test()
      self.logger.info("Assertion {}/{}({}) executed without errors. Iteration: {}({})".format(component_name, assertion_type, assertion_uuid, i, iteration_uuid))
      time.sleep(self.interval)

  def check_object(self):
    """
    Check assertion is associated to a component and has a uuid.
    """
    component_name = getattr(self.assertion, "component_name", "")
    if not len(component_name):
      raise RuntimeError("Assertion object has no component name.")

    uuid = getattr(self.assertion, "uuid", "")
    if not len(uuid):
      raise RuntimeError("Assertion object has no uuid. You are probably missing a super call on your __init__ method.")
