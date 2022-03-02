import boto3

import json
import io

from datetime import date

import pandas as pd

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Apartments')
def lambda_handler(event, context):
    
    #response = table.get_item(
    # Key={
    #    'ApartmentId': "de766e50-7d0a-4ffc-87d1-e429baedb42e",
    #    'CNT_NAME' : "Małopolskie",
    #})
    #item = response['Item']
    #print(item)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    df = pd.DataFrame(data)
    #print(item)
    print(df)
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    
    
    io_buffer = io.BytesIO()
    
    writer = pd.ExcelWriter(io_buffer, engine='xlsxwriter')
    sheets_in_writer=['Sheet1']
    
    data_frame_for_writer=[df]
    
    for i,j in zip(data_frame_for_writer,sheets_in_writer):
        i.to_excel(writer,j,index=False)
    
    ### Assign WorkBook
    workbook=writer.book
    
    # Add a header format
    header_format = workbook.add_format({'bold': True})
    max_col=3
    
    ### Apply same format on each sheet being saved
    for i,j in zip(data_frame_for_writer,sheets_in_writer):
        for col_num, value in enumerate(i.columns.values):
            writer.sheets[j].set_column(0, max_col - 1, 12)
            writer.sheets[j].write(0, col_num, value, header_format)
            writer.sheets[j].autofilter(0,0,0,i.shape[1]-1)
            writer.sheets[j].freeze_panes(1,0)
    writer.save()
    
    bucket = 'apartments-emigrants' 
    filepath = 'output/ExcelExample{}.xlsx'.format(d2)
    
    data = io_buffer.getvalue()        
    
    s3.Bucket(bucket).put_object(Key=filepath, Body=data)
    
    return  {
        'statusCode': 200,  
        'body': json.dumps(filepath)
        }