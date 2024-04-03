import os
import requests
import json
import paramiko

def get_currency_exchange_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error while receiving data")
        return None

def save_json_to_file(data, filepath):
    with open(filepath, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Data successfully saved to a file")

def send_file_to_ec2_instance(ec2_instance_ip, ec2_username, private_key_path, local_file, remote_file):
    ssh = paramiko.SSHClient()
    private_key = paramiko.RSAKey(filename=private_key_path)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ec2_instance_ip, username=ec2_username, pkey=private_key)
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        print(f"File {local_file} successfully sent to EC2 instance at {remote_file}.")
    except Exception as e:
        print(f"Error while sending file to EC2 instance: {e}")
    finally:
        ssh.close()

def main():
    json_file_path = input("Enter the path to save the JSON file: ")
    ec2_instance_ip = input("Enter the EC2 instance IP address: ")
    ec2_username = input("Enter the username for connecting to the EC2 instance: ")
    private_key_path = input("Enter the path to your private key (PEM): ")

    currency_exchange_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    data = get_currency_exchange_data(currency_exchange_url)

    if data:
        save_json_to_file(data, json_file_path)
        object_file_path = input("Enter the path to object file: ")
        send_file_to_ec2_instance(ec2_instance_ip, ec2_username, private_key_path, json_file_path, object_file_path)

if __name__ == "__main__":
    main()
