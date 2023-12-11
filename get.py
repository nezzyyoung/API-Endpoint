from collections import UserString
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import Flask, request, Response

app = Flask(__name__)

# AWS configuration
aws_access_key_id = 'AKIA2TMZO3HMKJMDGOG5'
aws_secret_access_key = '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'
aws_region = 'us-east-1'

dynamodb = boto3.resource('dynamodb',
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

def get_item(users, key):
    table = dynamodb.Table(users)

    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return None

@app.route('/get_data', methods=['GET'])
def get_data():
    if request.method == 'GET':
        try:
            table_name = 'users'
            key = {'104': 'caleb'}
            item = get_item(UserString, key)

            if item:
                return Response(json.dumps(item), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'error': 'Item not found'}), status=404, mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)