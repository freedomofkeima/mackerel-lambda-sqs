#!/usr/bin/env python
from mackerel.client import Client
import boto3
import json
import time

def handler(event, context):
    with open('conf.json') as data_file:
        data = json.load(data_file)
    # Create Mackerel client
    mackerel_client = Client(mackerel_api_key=data['mackerel_api_key'])
    # Get current time
    epoch_time = int(time.time())
    # Iterate through all services
    metrics = []
    for service in data['services']:
        type = service['aws_client_type']
        if type == 'sqs':
            client = boto3.client('sqs', region_name = service['aws_region'])
            response = client.get_queue_attributes(
                QueueUrl = service['queue_url'],
                AttributeNames=[service['sqs_attribute_name']]
            )
            # Process response to a metric value
            result = {}
            result['name'] = service['mackerel_metrics_name']
            result['time'] = epoch_time
            value = response['Attributes'][service['sqs_attribute_name']]
            if service['int_or_float'] == 'int':
                result['value'] = int(value)
            elif service['int_or_float'] == 'float':
                result['value'] = float(value)
            else:
                print "Value must be an integer or float"
            # Append metrics
            metrics.append(result)
        else:
            print "Type %s Not Implemented" % type
    # Post custom metrics
    mackerel_client.post_service_metrics(data['mackerel_service_name'], metrics)
    return "finished"
