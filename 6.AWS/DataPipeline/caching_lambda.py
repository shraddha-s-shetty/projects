import json
import boto3
import time

def update_dynamo_db_table(bucket_name,object_key,eventTime):
    s3_folder = object_key.split("/")[1]
    s3_parent_folder = object_key.split("/")[0]
    dynamo_db_table_name = f"App1-{bucket_name}-{s3_parent_folder}-dynamo"
    dynamodb = boto3.client('dynamodb')
    timestamp = str(eventTime)
    try:
        response = dynamodb.create_table(
            TableName=dynamo_db_table_name,
            KeySchema=[
                {
                    'AttributeName': 's3_folder',
                    'KeyType': 'HASH'  # Partition key
                },
                # Add other key attributes if required
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 's3_folder',
                    'AttributeType': 'S'  # String data type for the partition key
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,  # Adjust read capacity units as needed
                'WriteCapacityUnits': 5  # Adjust write capacity units as needed
            }
        )
        resp = response['TableDescription'] if 'TableDescription' in response else None
        time.sleep(5)
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Error: Table '{dynamo_db_table_name}' already exists.")
    except Exception as e:
        print(f"Error: {e}")
    
    items = [{
                's3_folder': {'S': s3_folder},
                's3_path': {'S': object_key},
                's3_timestamp': {'S': timestamp},
                'status': {'S': 'unprocessed'}
            }]
    for item in items:
        try:
            response = dynamodb.put_item(
                TableName=dynamo_db_table_name,
                Item=item
            )
            print(f"Item {item} added successfully.")
        except Exception as e:
            print(f"Error putting item {item}: {e}")

def lambda_handler(event, context):
    # TODO implement
    print(event)
    for item in event['Records']:
        bucket_name = item['s3']['bucket']['name']
        object_key = item['s3']['object']['key']
        event_time = item['eventTime']
        print(bucket_name)
        print(object_key)
        update_dynamo_db_table(bucket_name,object_key,event_time)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
