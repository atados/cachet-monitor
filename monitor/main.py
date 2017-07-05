from .component import Component
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
    component = Component(component_name, assertions)
    component.start()
