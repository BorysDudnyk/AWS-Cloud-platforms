import pandas as pd
import matplotlib.pyplot as plt
import boto3
from io import BytesIO

# Введення імені бакета
bucket_name = input("Name S3 bucket: ")

# Вбедення імені файлу вручну або автоматично
file_name = input("Name file picture.png: ")

csv_path = "/home/ec2-user/lab-2/curs_valut_lab2.csv"
df = pd.read_csv(csv_path, delimiter=",")

# відфільтруйте дані тільки для євро і доларів США
filtered_df = df[df["cc"].isin(["EUR", "USD"])]

plt.figure(figsize=(8, 8))
bars = plt.bar(filtered_df["cc"], filtered_df["rate"], color=("purple", "yellow"))
for bar, rate in zip(bars, filtered_df["rate"]):
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 0.01, f'{rate:.4f}', ha='center', va='bottom')
plt.title("Currency Exchange Rates for EUR and USD")
plt.xlabel("Currency Code")
plt.ylabel("Exchange Rate")
plt.xticks(rotation=45)

# збереження графіка в об'єкт BytesIO
buffer = BytesIO()
plt.savefig(buffer, format="png")
buffer.seek(0)

# Задайте шлях до S3 bucket
s3_path = f'{bucket_name}/{file_name}'

# Завантажте графік на S3
s3 = boto3.client('s3')
s3.upload_fileobj(buffer, bucket_name, file_name)

# Закрийте графік
plt.close()

# Друк шляху до завантаженого файлу
print(f'Graph saved to S3 bucket: s3://{s3_path}')
