class PerformanceProblems(BaseException):
  """
  Raised by assertions when a performance problem is detected
  """
  pass

class PartialOutage(BaseException):
  """
  Raised by assertions when there is a partial outage in a component
  """
  pass

class CompleteOutage(BaseException):
  """
  Raised by assertions when there is a complete outage in a component
  """
  pass
