from .utils import import_from_string
from .worker import WorkerThread
import shortuuid
import logging
import sys


def setup_logger(logging_level, logging_handler):
  """
  Create and configure logger
  """
  logger = logging.getLogger("monitor")
  logger.setLevel(logging_level)

  if not logging_handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def start_monitoring(tests, logging_level=logging.DEBUG, logging_handler=None):
  """
  Start monitoring threads
  """
  setup_logger(logging_level=logging_level, logging_handler=None)

  for component_name, assertions in tests.items():
    for assertion in assertions:
      AssertionClass = import_from_string(assertion["assertion"])
      kwargs = assertion.get("kwargs", {})
      settings = assertion.get("settings", {})

      assertion_object = AssertionClass(**kwargs)
      assertion_object.set_component_name(component_name)

      name = settings.get("name", shortuuid.uuid())
      assertion_object.set_friendly_name(name)

      thread = WorkerThread(assertion_object, interval=settings.get("interval", 1*60))
      thread.start()
