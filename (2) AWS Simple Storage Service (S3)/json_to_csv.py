import json
import pandas as pd
import boto3
from io import BytesIO

aws_access_key = 'AKIAZI2LGBBICD3XWNGU'
aws_secret_key = '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'

json_path = input("Enter the path to the JSON file: ")
bucket_name = input("Enter the S3 bucket name: ")
key = input("Enter the file name in S3 (e.g., output.csv): ")

with open(json_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    
df = pd.DataFrame(data)

csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False, encoding="utf-8")
          
csv_buffer.seek(0)
          
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
s3.upload_fileobj(csv_buffer, bucket_name, key)
          
print(f"Data from JSON file successfully uploaded to Amazon S3! {bucket_name}/{key}")
