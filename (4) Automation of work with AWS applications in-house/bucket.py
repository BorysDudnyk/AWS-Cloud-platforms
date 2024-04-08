import boto3

def create_bucket():
    s3 = boto3.client('s3')
    
    bucket_name = input("Введіть ім'я бакету: ")
    region = input("Введіть назву регіону (наприклад, us-east-1): ")
    
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        print(f"Бакет {bucket_name} успішно створений в регіоні {region}.")
    except Exception as e:
        print("Виникла помилка при створенні бакету:", str(e))

def delete_bucket():
    s3 = boto3.client('s3')
    
    bucket_name = input("Введіть ім'я бакету для видалення: ")
    
    try:
        response = s3.delete_bucket(Bucket=bucket_name)
        print(f"Бакет {bucket_name} успішно видалений.")
    except Exception as e:
        print("Виникла помилка при видаленні бакету:", str(e))

if __name__ == "__main__":
    create_bucket()
    delete_bucket()
