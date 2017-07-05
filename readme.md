getting started:
- pip install
- create settings and main
- deploy :)

assertions
Assertions are tests ran by the monitor to make sure the component is working. You can use default assertions or declare your own.

statuses
Component statuses are determined by the assertions used.
There are three kinds of exceptions an assertion can raise:
TestFailed: Self explanatory. This means the assertion has failed. There might be something wrong with the component.
CompleteOutage: This means the asserting is saying the component is completely down. You don't usually raise it unless you're sure the component is down.
ResponsePRoblems: The assertion detected a problem with response times.

If none of the assertions raise any exceptions, the component status will be set to "Completely Operational"
If at least one assertion for a given component raises TestFailed, the component status will be set to "Partial outage"
If all assertions for a given component raises TestFailed or ResponseProblems, the component status will be set to complete outage
If at least one assertions raises ResponseProblems and none raise TestFailed, the component status will be "delayed response"
