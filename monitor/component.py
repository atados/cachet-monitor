from .utils import import_from_string
from .worker import WorkerThread
from .status import *
import threading
import shortuuid
import logging

class Component():
  def __init__(self, name, assertions):
    self.name = name
    self.assertions = assertions
    self.history = {}
    self.last_status = None
    self.logger = logging.getLogger('monitor')

  def start(self):
    """
    Start threads for all assertions declared for a given component.
    """
    lock = threading.Lock()
    for assertion in self.assertions:
      AssertionClass = import_from_string(assertion["assertion"])
      kwargs = assertion.get("kwargs", {})
      settings = assertion.get("settings", {})

      assertion_object = AssertionClass(**kwargs)
      assertion_object.set_component_name(self.name)

      name = settings.get("name", shortuuid.uuid())
      assertion_object.set_friendly_name(name)

      thread = WorkerThread(
        assertion_object,
        assertion_executed_event=self.assertion_executed_event,
        interval=settings.get("interval", 1*60),
        lock=lock
      )
      thread.start()

  def assertion_executed_event(self, uuid, result):
    """
    This method is called by the Worker thread everyime a asserntion is ran
    to inform the component about the result of the test.

    Please note we call self.update_component_status which modifies shared data,
    therefore we need to acquire and release a lock when calling it.
    """
    self.history[uuid] = result
    self.update_component_status()

  def update_component_status(self):
    """
    Calls the API to update the component status if it has changed
    """
    status = self.determine_component_status()
    if status != self.last_status:
      self.logger.info("Component {} status has changed to {}".format(self.name, status))
      self.last_status = status

  def determine_component_status(self):
    """
    Determine the component status by the history of tests
    """
    data = {
      ASSERTION_SUCCESSFUL: 0,
      ASSERTION_FAILED: 0,
      ASSERTION_PERFORMANCE_PROBLEMS: 0,
      ASSERTION_COMPLETE_OUTAGE: 0,
    }
    for uuid, result in self.history.items():
      data[result] += 1

    # If no assertion raises exceptions, component is operational
    if data[ASSERTION_FAILED] == 0 and data[ASSERTION_PERFORMANCE_PROBLEMS] == 0 and data[ASSERTION_COMPLETE_OUTAGE] == 0:
      return COMPONENT_OPERATIONAL

    # If at least one assertion raises CompleteOutage, we force component status
    # to complete outage even if other assertions are successful
    if data[ASSERTION_COMPLETE_OUTAGE] > 0:
      return COMPONENT_COMPLETE_OUTAGE

    # Only response problems have been raised
    if data[ASSERTION_PERFORMANCE_PROBLEMS] > 0 and data[ASSERTION_FAILED] == 0:
      return COMPONENT_RESPONSE_PROBLEMS

    # There's an actual outage
    # Complete outage
    if data[ASSERTION_FAILED] > 0 and data[ASSERTION_SUCCESSFUL] == 0:
      return COMPONENT_COMPLETE_OUTAGE

    # Partial outage
    if data[ASSERTION_FAILED] > 0 and data[ASSERTION_SUCCESSFUL] != 0:
      return COMPONENT_PARTIAL_OUTAGE
