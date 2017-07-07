why:
Cachet is a well-known opensource status page system. Despite its fame, it lacks one essential thing: automated component testing. This is by design, instead, Cachet provides you with an API. Although the API is useful, you're left on your own to detect problems on components and report them back to Cachet. This project is an attempt to close this gap.

how
cachet-monitor is a python module which does the heavy lifting of executing automated assertions periodically and reporting them back to Cachet.

getting started:
- pip install
- create settings and main
- deploy :)

assertions
Assertions are tests ran by the monitor to make sure the components are working. cachet-monitor ships with common pre-defined assertions and can be easily extended to monitor any service you want.
There are three kinds of exceptions an assertion can raise:
TestFailed: Self explanatory. This means the assertion has failed. 
CompleteOutage: This means the asserting is saying the component is completely down. You don't usually raise it unless you're sure the component is down.
ResponsePRoblems: The assertion detected a problem with response times.

statuses
Component statuses are determined by the assertions used. A component can have 4 different status in Cachet

Operational
The component will assume this status if all assertions are executed sucessfuly.

Partial Outage
The component will assume this status if at least one assertion fails.

Complete Outage
The component will assume this status either if all assertion fail or a given assertion explicitly raise an CompleteOutage exception.

Performance Problems
The component will assume this status if at least one PerformanceProblem exception is raised and there are no failed assertions.

If none of the assertions raise any exceptions, the component status will be set to "Completely Operational"
If at least one assertion for a given component raises TestFailed, the component status will be set to "Partial outage"
If all assertions for a given component raises TestFailed or ResponseProblems, the component status will be set to complete outage
If at least one assertions raises ResponseProblems and none raise TestFailed, the component status will be "delayed response"
