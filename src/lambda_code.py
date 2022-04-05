# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import boto3
from botocore.config import Config
from region_lookup import active_region

__active_region = active_region()

my_config = Config(
    region_name = __active_region
)

client = boto3.client('health', config = my_config)
code_pipeline = boto3.client('codepipeline')

def lambda_handler(event, context):
    
    ## Either pass the region from CodePipeline or manually configure in the Lambda function. 
    regions = ""
    # Case1: Pass UserParameters from CodePipeline as a comma separated string
    if "UserParameters" in event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"]:
        regions = (event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"]["UserParameters"]).split(",")
    
    # Case2: If regions are not passed from CodePipeline, set it manually in the regions array. 
    if regions == "":
        regions = ["us-east-1"]
    
    response = fetch_health_events(regions)
    
    incidentInProgress = False
    
    job = event["CodePipeline.job"]["id"]
    if(response["events"] == []):
        incidentInProgress = False
        code_pipeline.put_job_success_result(jobId=job)
    else:
        incidentInProgress = True
        code_pipeline.put_job_failure_result(jobId=job, failureDetails={'message': 'Incident In Progress', 'type': 'JobFailed'})
    
def fetch_health_events(regions):
    response = client.describe_events(
    filter={
        'regions': regions,
        'eventTypeCategories': [
            'issue'
        ],
        'eventStatusCodes': [
            'open','upcoming'
        ]
    }
)
    
    return response