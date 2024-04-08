import boto3

def create_key_pair():
    ec2 = boto3.client('ec2')
    
    key_name = input("Введіть ім'я ключа: ")

    try:
        response = ec2.create_key_pair(KeyName=key_name)
        with open(f"{key_name}.pem", "w") as key_file:
            key_file.write(response['KeyMaterial'])
        print(f"Пара ключів {key_name} успішно створена. Ключ збережено в файлі {key_name}.pem")
    except Exception as e:
        print("Виникла помилка при створенні пари ключів:", str(e))

if __name__ == "__main__":
    create_key_pair()
