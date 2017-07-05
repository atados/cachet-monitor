import threading
import time
import logging
import shortuuid

class WorkerThread(threading.Thread):
  def __init__(self, assertion, interval=1*60):
    super(WorkerThread, self).__init__()
    self.assertion = assertion
    self.interval = interval
    self.logger = logging.getLogger('monitor')

  def run(self):
    """
    Called when thread is started.
    """
    self.check_object()
    self.loop()

  def loop(self):
    """
    This method loops forever executing the assertion test method.
    """
    friendly_name = self.assertion.friendly_name
    component_name = self.assertion.component_name
    assertion_type = type(self.assertion).__name__

    i = 0
    while True:
      i += 1

      self.logger.info(
          "Running assertion {}/{}({}). Iteration: {}"
          .format(component_name, component_name, friendly_name, i)
      )
      self.assertion.test()
      self.logger.info(
          "Assertion {}/{}({}) executed without errors. Iteration: {}"
          .format(component_name, component_name, friendly_name, i)
      )

      time.sleep(self.interval)

  def check_object(self):
    """
    Check assertion is associated to a component and has an uuid.
    """
    component_name = getattr(self.assertion, "component_name", "")
    if not len(component_name):
      raise RuntimeError("Assertion object has no component name.")

    friendly_name = getattr(self.assertion, "friendly_name", "")
    if not len(friendly_name):
      raise RuntimeError("Assertion object has no friendly_name.")
