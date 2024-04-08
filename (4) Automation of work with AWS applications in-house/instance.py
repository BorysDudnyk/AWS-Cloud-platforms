
import boto3

def create_instance():
    ec2 = boto3.resource('ec2')
    
    instance_type = input("Введіть тип інстансу: ")
    ami_id = input("Введіть ID образу AMI: ")
    key_name = input("Введіть ім'я ключа: ")
    instance_name = input("Введіть ім'я інстансу: ")
    
    try:
        instance = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': instance_name}]}] 
        )[0]
        print(f"Інстанс {instance.id} з ім'ям {instance_name} успішно створений.")
    except Exception as e:
        print("Виникла помилка при створенні інстансу:", str(e))

def start_instance():
    ec2 = boto3.resource('ec2')
    
    instance_id = input("Введіть ID інстансу для запуску: ")
    
    try:
        instance = ec2.Instance(instance_id)
        instance.start()
        print(f"Інстанс {instance_id} успішно запущений.")
    except Exception as e:
        print("Виникла помилка при запуску інстансу:", str(e))

def stop_instance():
    ec2 = boto3.resource('ec2')
    
    instance_id = input("Введіть ID інстансу для зупинки: ")
    
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        print(f"Інстанс {instance_id} успішно зупинений.")
    except Exception as e:
        print("Виникла помилка при зупинці інстансу:", str(e))

def delete_instance():
    ec2 = boto3.resource('ec2')
    
    instance_id = input("Введіть ID інстансу для видалення: ")
    
    try:
        instance = ec2.Instance(instance_id)
        instance.terminate()
        print(f"Інстанс {instance_id} успішно видалений.")
    except Exception as e:
        print("Виникла помилка при видаленні інстансу:", str(e))

if __name__ == "__main__":
    create_instance()
    start_instance()
    stop_instance()
    delete_instance()
