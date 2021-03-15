import json
import os

import boto3

from cookbook.backends.dynamo import DynamoBackend
from cookbook.cookbook import Cookbook, CookbookException
from cookbook.util import get_test_table

# Use this as our key that we're running locally
if 'AWS_EXECUTION_ENV' not in os.environ:
    table = get_test_table('us-east-2', 'http://127.0.0.1:8000', 'cookbook-recipes-dev')
    cookbook = Cookbook(DynamoBackend(table))
else:
    ddb = boto3.resource('dynamodb')
    cookbook = Cookbook(DynamoBackend(ddb.Table(os.environ['DYNAMODB_TABLE'])))


# https://www.restapitutorial.com/lessons/httpmethods.html
# /recipes/ (get, post)
# /recipes/${id} (get, put, delete)

# Using the lambda-proxy integration mode
# https://www.serverless.com/framework/docs/providers/aws/events/apigateway#example-lambda-proxy-event-default

def get_body(event):
    body = event.get('body')
    return json.loads(event.get('body')) if isinstance(body, str) else {}


# Collect Body & ID
def request_runner(function, event, context):
    body = get_body(event)
    recipe_id = event.get('requestPath').split('/')[-1]

    try:
        fxn = getattr(cookbook, function)
        # Responses from functions are either ids, or recipe bodies
        # Inputs are either body or id
        resp = fxn(body | recipe_id)
    except CookbookException as e:
        body = {
            'errors': e.messages
        }

    response = {
        # This can be param'd probably based on error content?
        'statusCode': 200 if recipe_id else 400,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response


def post(event, context):
    body = get_body(event)
    try:
        recipe_id = cookbook.save(body)
        body = {
            'id': recipe_id
        }
    except CookbookException as e:
        body = {
            'errors': e.messages
        }

    response = {
        'statusCode': 201 if recipe_id else 400,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response


# TODO: Implement Pagination b/c it annoys you when its not there
def list(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(cookbook.list()),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def get(event, context):
    recipe_id = event.get('requestContext').get('path').split('/')[-1]
    try:
        body = cookbook.read(recipe_id)
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        'statusCode': 200 if 'errors' not in body else 404,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response


# hoooooo these error codes are not gonna be good friend
def put(event, context):
    body = get_body(event)
    body.update(id=event.get('requestContext').get('path').split('/')[-1])
    try:
        recipe_id = cookbook.save(body)
        body = {
            'id': recipe_id
        }
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        'statusCode': 201 if 'errors' not in body else 400,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response


def delete(event, context):
    recipe_id = event.get('requestContext').get('path').split('/')[-1]
    try:
        recipe_id = cookbook.delete(recipe_id)
        body = {
            'id': recipe_id
        }
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        'statusCode': 200 if 'errors' not in body else 400,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response
