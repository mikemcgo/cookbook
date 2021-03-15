# cookbook

This project serves as a learning experience on how to deploy a simple recipe storage app in a variety of technologies and methodologies.

Welcome to the most over-analyzed and over-tested crud app. Well fine, it doesn't do 'exciting testing' like fuzzing, performance, etc...

## serverless framework

The experience around this tool is not as good as I remember, particularly around local testing and dynamodb. The `serverless-dynamodb-local` plugin seems to simply not work, although I can't figure out why. I suspected it was due to table encryption but removing it didn't fix the problem so I have no idea.

Additionally, using the `serverless-offline` plugin wasn't as helpful as I remember it being. I've broken some logic with pycharm and am unable to run multiple test suites without resetting the local environment. There are also some discrepancies around what the offline lambdas return, and what the AWS based API Gateways return, which concerns me. Upon further inspection, might have had things mis-configured as the api gw response has the full body including response code. Is probably also related to the lambda integration types with api gateway. Moving towards lambda-proxy instead of 'lambda'.

Kinda concluding local dev isn't great with serverless, which bothers me, but also might be because of personal bias. Properly config'd AWS account and ci/cd based against the account would probably be fine, just a bit lazy to do that right now, and would prefer to be able to use pycharm to debug instead of fighting logs in Amazon.

At one point this was the local integration test runner:

```
#!/bin/sh

serverless offline start &

sleep 6

pytest tests/integration/serverless

pgrep node | xargs kill -9
```

Probably can make a local test shim that simulates the api gateway vaguely for testing purposes and then just yayeet that thing into the account for now. This approach seems to be working decently well? Granted theres only like 5 endpoints to route to, so meh. Was able to duck type my way into tests that can either run locally through the shim, or remotely against the api gateway.

And now I recall that this is built on cloudformation, and that I don't like cloudformation. Somehow borked the cf stack trying to rip out the kms key (since I'm getting charged for it), and now I have to kill the whole stack in the console and restart.