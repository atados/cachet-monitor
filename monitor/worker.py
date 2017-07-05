from .exceptions import *
from .status import *
import threading
import time
import logging
import shortuuid

class WorkerThread(threading.Thread):
  def __init__(self, assertion, assertion_executed_event, lock, interval=1*60):
    super(WorkerThread, self).__init__()
    self.assertion = assertion
    self.interval = interval
    self.assertion_executed_event = assertion_executed_event
    self.lock = lock
    self.logger = logging.getLogger('monitor')
    self.check_object()

  def run(self):
    """
    Called when thread is started.
    """
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
          "Running assertion {}/{}. Iteration: {}"
          .format(component_name, friendly_name, i)
      )

      try:
        result = self.run_assertion()
      except Exception as e:
        self.logger.error(
            """Assertion {}/{} raised an exception different than PerformanceProblems, TestFailed and CompleteOutage. Iteration: {}\n
            All error treatment should be done inside the assertion .test method. The assertion will be defined as failed but that doesn't mean
            there is a problem with the component. The problem might be in your assertion code.\n
            {}: {}"""
            .format(component_name, friendly_name, i, e.__class__.__name__, e)
        )
        result = ASSERTION_FAILED

      if result == ASSERTION_SUCCESSFUL:
        self.logger.info(
            "Assertion {}/{} executed without errors. Iteration: {}"
            .format(component_name, friendly_name, i)
        )
      if result == ASSERTION_FAILED:
        self.logger.warning(
            "Assertion {}/{} failed. Iteration: {}"
            .format(component_name, friendly_name, i)
        )
      if result == ASSERTION_COMPLETE_OUTAGE:
        self.logger.warning(
            "Assertion {}/{} reported complete outage. Iteration: {}"
            .format(component_name, friendly_name, i)
        )

      self.lock.acquire()
      self.assertion_executed_event(uuid=self.assertion.uuid, result=result)
      self.lock.release()

      time.sleep(self.interval)

  def run_assertion(self):
    """
    Run assertion test method and detect if it was or wasn't successful
    """
    try:
      self.assertion.test()
    except PerformanceProblems:
      return ASSERTION_PERFORMANCE_PROBLEMS
    except TestFailed:
      return ASSERTION_FAILED
    except CompleteOutage:
      return ASSERTION_COMPLETE_OUTAGE
    return ASSERTION_SUCCESSFUL

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

    uuid = getattr(self.assertion, "uuid", "")
    if not len(uuid):
      raise RuntimeError("Assertion object has no uuid. You're probably missing the super call on your __init__ method.")
