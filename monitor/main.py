from .utils import import_from_string

def start_monitoring(tests):
  """
  Start monitoring threads
  """
  for component, assertions in tests.items():
    print(component)
