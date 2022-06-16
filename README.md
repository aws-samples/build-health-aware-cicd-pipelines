# AWS Health Aware CI/CD Pipelines
This is a step by step guide on how to deploy and integrate the AWS Health Aware CI/CD Pipelines [blog post](https://aws.amazon.com/blogs/devops/build-health-aware-ci-cd-pipelines/) sample code on AWS Lambda through the AWS Console and CLI. 

## Build

1. Create a directory for your build
`mkdir package`

2. Install the dependencies
`pip install -r requirements.txt --target ./package`

3. Copy the *src/lambda_code.py* and *src/region_lookup.py* to the package folder

4. Create the deployment package
`cd package`
`zip -r ../deployment-package-v1.0.py .` 

## Deploy

From the AWS Console or CLI, follow the steps in the [AWS Lambda guide](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) to deploy the ZIP archive to a Lambda function. Attach the lambda-execution-role-policy.json policy to your Lambda Execution role to grant required permissions. 

## User Guide

In order to integrate the Lambda function code, set the `regions` array in `lambda_handler` under `lambda_code.py`. `regions` is used to filter health events in a specific region(s). Filtering health events in the same region as the pipeline is essential to avoid false signals. 

In case of CodePipeline, make use of `UserParameters` in order to pass region information to the Lambda function. Set `UserParameters` as a comma-separated string (i.e. us-east-1,ap-southeast-2). Implicitly, `lambda_handler` converts the string into a string array. 

If `UserParameters` is not set, the Lambda function falls back to a pre-defined list of regions configured in the `regions` array. 

For further context, follow the guidance in the blog post for guidance on how integrate the Lambda function into your solution. 
