from monitor.exceptions import *
import shortuuid

class BaseAssertion():
  def set_friendly_name(self, friendly_name):
    """
    Set a friendly name to the assertion. This is useful so you can recognize the assertion in logs.
    """
    self.friendly_name = friendly_name

  def set_component_name(self, component_name):
    """
    Set component name so the assertion knows which component to report to.
    """
    self.component_name = component_name

  def test(self):
    """
    This method should implement the assertion for the component.

    In case of test failure, you should raise either PerformanceProblems,
    PartialOutage or CompleteOutage.
    """
    raise NotImplemented("The .test method must be overriden.")

  def raise_performance_problems(self):
    raise PerformanceProblems()

  def raise_partial_outage(self):
    raise PartialOutage()

  def raise_complete_outage(self):
    raise CompleteOutage()

  def raise_default_exception(self):
    pass
