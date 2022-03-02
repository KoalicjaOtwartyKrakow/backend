import simplejson as json
import uuid
import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Apartments')
    print(event)
    body = json.loads(event['body'])
    guid = str(uuid.uuid4())
    try:
        table.put_item(
        Item={
            'ApartmentId': guid,
            'CNT_NAME': body['CNT_NAME'].upper(),
            'CITY': body['CITY'].upper(),
            'ZIP': body['ZIP'],
            'DESCRIPTION': body['DESCRIPTION'],
            'LANDLORD_PHONE': body['LANDLORD_PHONE'],
            'LANDLORD_EMAIL': body['LANDLORD_EMAIL'],
            'PLACES_NUM': body['PLACES_NUM'],
            'PLACES_BUSY': 0,
            'LANDLORD_NAME': body['LANDLORD_NAME'],
            'ST_NAME': body['ST_NAME'].upper(),
            'ST_NUM': body['ST_NUM'],
            'APT_NUM': body['APT_NUM'],
            'VOLUNTEER_NAME': "",
            'IS_VERIFIED': False,
            'CreationTime': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        )
    except Exception as e:
        print(e)
        print(e.args)
        return {
            'statusCode': 503,
            'body': json.dumps(str(e))
        }
    
    response = table.get_item(
        Key={
            'ApartmentId': guid,
            'CNT_NAME': body['CNT_NAME'],
        }
    )
    item = response['Item']
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
