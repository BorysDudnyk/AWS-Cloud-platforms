import boto3

def download_file_from_s3(bucket_name, object_key, local_file_path):
    s3 = boto3.client('s3')
    
    try:
        s3.download_file(bucket_name, object_key, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
    except Exception as e:
        print (f"Error downloading file: {e}")
def main_func ():
    bucket_name = input("Enter the S3 bucket name: ")
    object_key = input("Enter the object key (file name) in S3: ")
    local_file_path = input("Enter the local file path to save the downloaded file: ")
    
    download_file_from_s3 (bucket_name, object_key, local_file_path)
    
main_func()
