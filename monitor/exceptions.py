class PerformanceProblems(BaseException):
  """
  Raised by assertions when a performance problem is detected
  """
  pass

class CompleteOutage(BaseException):
  """
  Raised by assertions when there is a complete outage in a component
  """
  pass

class TestFailed(BaseException):
  """
  Raised by assertions when the assetion fails
  """
  pass
