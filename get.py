import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import Flask, request, Response

app = Flask(__name__)

# AWS configuration
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'
aws_region = 'your_region'

dynamodb = boto3.resource('dynamodb',
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

def get_item(table_name, key):
    table = dynamodb.Table(table_name)

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
            table_name = 'your_table_name'
            key = {'your_primary_key': 'value'}
            item = get_item(table_name, key)

            if item:
                return Response(json.dumps(item), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'error': 'Item not found'}), status=404, mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)