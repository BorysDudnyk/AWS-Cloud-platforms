import pandas as pd
import matplotlib.pyplot as plt
import boto3
from io import BytesIO

csv_path = '/home/ec2-user/lab-2/curs_valut_lab2.csv'

df = pd.read_csv(csv_path, delimiter=',')

plt.figure(figsize=(30, 8))
bars = plt.bar(df['cc'], df['rate'], color='blue')

for bar, rate in zip(bars, df['rate']):
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 0.01, f'{rate:.4f}', ha='center', va='bottom')

plt.title('Currency Exchange Rates')
plt.xlabel('Currency Code')
plt.ylabel('Exchange Rate')
plt.xticks(rotation=45)

plt.subplots_adjust(bottom=0.3)
plt.show()
