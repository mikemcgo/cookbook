import json
import os

import boto3

from cookbook.backends.dynamo import DynamoBackend
from cookbook.cookbook import Cookbook, CookbookException

ddb = boto3.resource('dynamodb')
cookbook = Cookbook(DynamoBackend(ddb.Table(os.environ["DYNAMODB_TABLE"])))


# https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-documenting-api.html

# https://www.restapitutorial.com/lessons/httpmethods.html
# https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway
# /recipes/ (get, post)
# /recipes/${id} (get, put, delete)

def post(event, context):
    body = json.loads(event.body)
    try:
        recipe_id = cookbook.save(body)
        body = {
            'recipe_id': recipe_id
        }
    except CookbookException as e:
        body = {
            'errors': e.messages
        }

    response = {
        "statusCode": 200 if recipe_id else 400,
        "body": body
    }

    return response


# TODO: Implement Pagination b/c it annoys you when its not there
def list(event, context):
    return {'statusCode': 201,
            'body': json.dumps(cookbook.list())}


def get(event, context):
    recipe_id = json.loads(event.body).get('id')
    try:
        body = cookbook.read(recipe_id)
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        "statusCode": 200 if 'errors' not in body else 404,
        "body": body
    }

    return response


# hoooooo these error codes are not gonna be good friend
def put(event, context):
    recipe_id = json.loads(event.body).get('id')
    try:
        body = cookbook.put(recipe_id)
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        "statusCode": 200 if 'errors' not in body else 404,
        "body": body
    }

    return response


def delete(event, context):
    recipe_id = json.loads(event.body).get('id')
    try:
        body = cookbook.delete(recipe_id)
    except CookbookException as e:
        body = {
            'errors': e.messages
        }
    response = {
        "statusCode": 200 if 'errors' not in body else 404,
        "body": body
    }

    return response
