import boto3

import json
import io

from datetime import date

import pandas as pd

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Apartments')

def upload_to_dynamodb(bucket, key):
    bucket_object = s3.get_object(Bucket=bucket,Key=key)
    content = bucket_object['Body'].read()
    df = pd.read_excel(io.BytesIO(content),engine = 'openpyxl')

    df.columns=["ZIP", "CITY", "DESCRIPTION", "LANDLORD_PHONE",	"ApartmentId", "LANDLORD_EMAIL", "PLACES_NUM", "LANDLORD_NAME", "CNT_NAME", "APT_NUM", "ST_NAME", "VOLUNTEER_NAME", "CreationTime", "PLACES_BUSY", "ST_NUM", "IS_VERIFIED"]
    # Clean-up the data, change column types to strings to be on safer side :)
    df=df.replace({'-': '0'}, regex=True)
    df=df.fillna(0)
    for i in df.columns:
        df[i] = df[i].astype(str)
    # Convert dataframe to list of dictionaries (JSON) that can be consumed by any no-sql database
    myl=df.T.to_dict().values()
    # Load the JSON object created in the step 3 using put_item method
    for permit in myl:
        print(permit)
        responce = table.put_item(Item=permit)
        print(responce)

def lambda_handler(event, context):
    bucket = 'apartments-emigrants'
    key = 'output/ExcelExampleFebruary 27, 2022_modify.xlsx'
    upload_to_dynamodb(bucket, key)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

