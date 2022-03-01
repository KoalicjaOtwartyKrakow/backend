import simplejson as json
import boto3
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    
    response = client.list_users(
        UserPoolId='eu-west-1_hU7IA1k0f',
        AttributesToGet=[
        'name',
        'phone_number',
        'email',
    ],
    )
    
    users = response['Users']
    print(users)
    ret = []
    for user in users:
        ret_user = {'Username': user['Username'], 'UserStatus': user['UserStatus']}
        for atr in user['Attributes']:
            ret_user[atr['Name']] = atr['Value']
        ret.append(ret_user)
    return {
        'statusCode': 200,
        'body': json.dumps(ret)
    }
