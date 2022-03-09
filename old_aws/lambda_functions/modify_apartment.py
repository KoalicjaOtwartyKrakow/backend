import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Apartments")
    body = json.loads(event["body"])
    table.update_item(
        Key={
            "ApartmentId": body["ApartmentId"],
            "CNT_NAME": body["CNT_NAME"].upper(),
        },
        UpdateExpression="SET CITY = :val1, ZIP = :val2, DESCRIPTION = :val3, LANDLORD_PHONE = :val4, LANDLORD_EMAIL = :val5, PLACES_NUM = :val6, PLACES_BUSY = :val7, LANDLORD_NAME = :val8, ST_NAME = :val9, ST_NUM = :val10, APT_NUM = :val11, VOLUNTEER_NAME = :val12, IS_VERIFIED = :val13",
        ExpressionAttributeValues={
            ":val1": body["CITY"].upper(),
            ":val2": body["ZIP"],
            ":val3": body["DESCRIPTION"],
            ":val4": body["LANDLORD_PHONE"],
            ":val5": body["LANDLORD_EMAIL"],
            ":val6": body["PLACES_NUM"],
            ":val7": body["PLACES_BUSY"],
            ":val8": body["LANDLORD_NAME"],
            ":val9": body["ST_NAME"].upper(),
            ":val10": body["ST_NUM"],
            ":val11": body["APT_NUM"],
            ":val12": body["VOLUNTEER_NAME"],
            ":val13": body["IS_VERIFIED"],
        },
    )
    response = table.get_item(
        Key={
            "ApartmentId": body["ApartmentId"],
            "CNT_NAME": body["CNT_NAME"],
        }
    )
    item = response["Item"]
    return {"statusCode": 200, "body": json.dumps(item)}
