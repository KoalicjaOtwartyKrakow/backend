import simplejson as json
import boto3
import base64

s3 = boto3.client('s3')
def lambda_handler(event, context):
    bucket = 'apartments-emigrants'
    key = 'Umowa.docx'
    response = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket,
                                                'Key': key},
                                                ExpiresIn=3600)
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
