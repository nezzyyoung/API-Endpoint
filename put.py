import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your_table_name')

def lambda_handler(event, context):
    try:
        response = table.put_item(
            Item={
                'id': event['id'],
                'name': event['name'],
                'email': event['email']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("PutItem succeeded!")

    return {
        'statusCode': 200,
        'body': json.dumps('Data saved to DynamoDB successfully!')
    }