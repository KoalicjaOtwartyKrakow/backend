import json
import boto3

client = boto3.client("cognito-idp")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    response = client.admin_confirm_sign_up(
        UserPoolId="eu-west-1_hU7IA1k0f", Username=body["Username"]
    )
    print(response)
    return {"statusCode": 200, "body": json.dumps("Verified")}
