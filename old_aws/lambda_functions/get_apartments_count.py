import simplejson as json
import boto3
import collections

s3 = boto3.resource("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Apartments")


def lambda_handler(event, context):
    response = table.scan()
    data = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    value_by_cnt = collections.Counter()
    value_by_cnt["TOTAL"] = {
        "TOTAL_USERS": 0,
        "TOTAL_PLACES": 0,
        "TOTAL_PLACES_BUSY": 0,
    }
    for d in data:
        if value_by_cnt[d["CNT_NAME"]] == 0:
            value_by_cnt[d["CNT_NAME"]] = {
                "TOTAL_USERS": 0,
                "TOTAL_PLACES": 0,
                "TOTAL_PLACES_BUSY": 0,
            }
        value_by_cnt["TOTAL"]["TOTAL_USERS"] += 1
        value_by_cnt["TOTAL"]["TOTAL_PLACES"] += d["PLACES_NUM"]
        value_by_cnt["TOTAL"]["TOTAL_PLACES_BUSY"] += d["PLACES_BUSY"]
        value_by_cnt[d["CNT_NAME"]]["TOTAL_USERS"] += 1
        value_by_cnt[d["CNT_NAME"]]["TOTAL_PLACES"] += d["PLACES_NUM"]
        value_by_cnt[d["CNT_NAME"]]["TOTAL_PLACES_BUSY"] += d["PLACES_BUSY"]
    return {"statusCode": 200, "body": json.dumps(value_by_cnt)}
