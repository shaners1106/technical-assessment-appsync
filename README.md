# Take Home Challenge: AWS AppSync
This exercise is meant to showcase your technical implementation & design abilities. 
**It is expected that you will fork this repository in GitHub** and share the link with us 
when complete. Please be prepared to explain the design.

For the purposes of the exercise, pretend you're on a team working on a new website that 
customers can use to look up information. Other team members are handling the 
front end, but you're working on the back-end API.

## Instructions

Implement a fully deployable GraphQL API using *AWS AppSync* can return the Mean, Median and Mode of a 
series of numbers. The actual logic for calculating these values can be implemented as 
*AWS Lambda* functions deployed alongside the AppSync API, inline code in VTL mapping 
templates, or inline code as JavaScript resolvers.

Bonus points awarded for the following:

- implementing a solution that leverages an AppSync *Pipeline Resolver* that
separates the logic for each of the different calculations into *Pipeline Functions*
- incorporating security for the API to use an API key generated during deployment.

The GraphQL schema for this API is provided in this repository, as well as the skeleton of the
*AWS CDK* stack that can be used as the starting point for implementing the deployment portion
of this challenge.

For reference, here is the AWS AppSync Developer Guide: https://docs.aws.amazon.com/appsync/latest/devguide

Please include instructions on how to run, test and deploy your code.
