import boto3
import os
from awsglue.utils import getResolvedOptions
import sys
import time


class GlueManager:
    def __init__(self):
        self.glue_client = boto3.client('glue')

    def check_database_existence(self,database_name):
        try:
            response = self.glue_client.get_database(Name=database_name)
            return True  
        except self.glue_client.exceptions.EntityNotFoundException:
            return False
        
    def create_glue_database(self,database_name, description=''):
        if not self.check_database_existence(database_name):
            response = self.glue_client.create_database(
                DatabaseInput={
                    'Name': database_name,
                    'Description': description
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
            else:
                raise ValueError("Error while creating database")
        else:
            return True
        
    def check_crawler_existence(self,crawler_name):
        try:
            response = self.glue_client.get_crawler(Name=crawler_name)
            return True  # Crawler exists
        except self.glue_client.exceptions.EntityNotFoundException:
            return False
        
    def cralwer_runner(self,s3_bucket,s3_parent_folder,s3_folder,database_name):
        crawler_name = s3_parent_folder.lower() + s3_folder
        s3_path= f's3://{s3_bucket}/{s3_parent_folder}/{s3_folder}'
        
        if not self.check_crawler_existence(crawler_name):
            response = self.glue_client.create_crawler(
                Name=crawler_name,
                Role='App1-glue-role',  # Replace with your IAM role
                DatabaseName=database_name,
                Targets={
                    'S3Targets': [
                        {
                            'Path': s3_path
                        }
                    ]
                },  # Example: Run every day at midnight UTC
                SchemaChangePolicy={
                    'UpdateBehavior': 'UPDATE_IN_DATABASE',
                    'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
                }
            )
            if response:
                print("Crawler created successfully")
            else:
                raise ValueError("Error while creating crawler")
        else:
            raise ValueError("Crawler not created error!")
        if self.check_run_crawler_status(crawler_name):
            try:    
                cralwer_resp = self.glue_client.start_crawler(Name=crawler_name)
                if self.check_run_crawler_status(crawler_name):
                    return cralwer_resp
            except Exception as e:
                raise e
        else:
            raise ValueError("Crawler start issue!")
        
    def check_run_crawler_status(self,crawler_name): 
        ###Check crawler status and wait if crawler is running
        while True:
            try:
                response = self.glue_client.get_crawler(Name=crawler_name)
                crawler_status = response['Crawler']['State']
                print(f"Crawler status is {crawler_status}")
            except self.glue_client.exceptions.EntityNotFoundException:
                raise ValueError("Crawler not found!")
            if crawler_status is None or crawler_status == 'READY':
                print(f"Crawler {crawler_name} is not running or finished.")
                # Start the crawler if it's not running
                return True
            elif crawler_status == 'RUNNING':
                print(f"Crawler {crawler_name} is still running. Waiting...")
                time.sleep(30)  # Wait for 30 seconds before checking again
            else:
                print(f"Unexpected status: {crawler_status}")
                return False
    
    def get_all_glue_tables(self,database_name):
        next_token = None
        tbl_list = []
        while True:
            # Retrieve tables from the Glue Data Catalog with pagination
            response = self.glue_client.get_tables(DatabaseName=database_name, NextToken=next_token)
            
            tables = response['TableList']
            tbl_list.append(tables)
                
            # Check if there are more pages of results
            if 'NextToken' in response:
                next_token = response['NextToken']
            else:
                break
        return tbl_list
        

class DynamoManager:

    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')

    def get_cached_details(self,bucket_name,s3_parent_folder):
        attribute_name = 'status'
        attribute_value = 'unprocessed'
        table_name = f"App1-{bucket_name}-{s3_parent_folder}-dynamo"
        print(table_name)
        try:
            response = self.dynamodb.scan(
                TableName=table_name,  # Replace with the non-primary key attribute name
                FilterExpression=f"#{attribute_name} = :val",
                ExpressionAttributeNames={f"#{attribute_name}": attribute_name},
                ExpressionAttributeValues={":val": {'S': attribute_value}}  # Adjust data type as needed
                )
            items = response['Items'] if 'Items' in response else []
            folder_names = [item.get('s3_folder', {}).get('S', '') for item in items]
            print(folder_names)
            return folder_names
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == '__main__':
    args = getResolvedOptions(sys.argv, ['JOB_RUN_ID','s3_bucket','s3_folder'])
    job_run_id = args["JOB_RUN_ID"]
    s3_bucket = args["s3_bucket"]
    s3_parent_folder = args["s3_folder"]
    glue_database_name = s3_parent_folder.lower()
    print(job_run_id)
    print(s3_bucket)
    print(s3_parent_folder)

    ###########################################################################
    # Usage examples
    dynamo_manager = DynamoManager()
    s3_folder_list = dynamo_manager.get_cached_details(bucket_name=s3_bucket,s3_parent_folder=s3_parent_folder)
    glue_manager = GlueManager()
    database_check = glue_manager.create_glue_database(database_name=glue_database_name)
    for item in s3_folder_list:
        crawler_response = glue_manager.cralwer_runner(s3_bucket=s3_bucket,s3_parent_folder=s3_parent_folder,s3_folder=item,database_name=glue_database_name)
        print("Crawler run response: ",crawler_response)
    ###########################################################################
    ###Convert csv files to parquet
    ###Go to glue tables get csv file classifiers if csv get s3 location 
    ###Now apply transformations and convert csv to parquet, small files with pandas and large files with pyspark
    list_glue_tables = glue_manager.get_all_glue_tables(glue_database_name)
    csv_s3_files = []
    for item in list_glue_tables:
        if 'csv' in item['StorageDescriptor']['Location']:
            csv_s3_files.append(item['StorageDescriptor']['Location'])
    
    for item in csv_s3_files:
        


    




    
    

