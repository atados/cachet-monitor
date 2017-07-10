from .component import Component
from .api import API
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


def start_monitoring(tests, api, logging_level=logging.DEBUG, logging_handler=None):
  """
  Start monitoring threads
  """
  setup_logger(logging_level=logging_level, logging_handler=None)
  api = API(**api)

  for component in tests:
    component_name = component.get("name", None)
    component_id = component.get("id", None)
    component_incidents = component.get("incidents", {})
    component = Component(component_name, component_id, component["assertions"], api, incidents=component_incidents)
    component.start()
