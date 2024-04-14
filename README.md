# Machine Learning in AWS Sagemaker: приклад на наборі даних bezdekIris

Цей проект демонструє основні елементи машинного навчання з використанням AWS Sagemaker на прикладі роботи з набором даних **bezdekIris**. Проект містить операції з підготовки даних, навчання моделі та прогнозування з використанням Sagemaker.

# План проекту

# 1. Імпорт бібліотек:
# Імпортуйте необхідні бібліотеки для роботи з AWS Sagemaker, AWS S3, обробки даних, візуалізації та машинного навчання.
import warnings
warnings.filterwarnings("ignore")
import boto3
from sagemaker import get_execution_role
import sys, os
import pandas as pd
import numpy as np
import sagemaker.amazon.common as smac
import io
from pathlib import Path
import shutil
from sklearn.model_selection import train_test_split
import json
from sklearn import metrics
from sagemaker.amazon.amazon_estimator import get_image_uri
import sagemaker
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import time
import matplotlib.pyplot as plt

# 2. Конфігурація Sagemaker:
# Налаштуйте середовище (SDK) для роботи з AWS Sagemaker.
sagemaker.config.INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config.INFO - Not applying SDK defaults from location: /home/ec2-user/.config/sagemaker/config.yaml

# 3. Змінні налаштувань:
# Визначте змінні для імен файлів, шляхів та S3-ковша для зберігання та доступу до даних.
filename = 'bezdekIris-dataset.data'
bucket = 'dataset-for-python'
raw_prefix = 'raw'
dataset_name = 'bezdekIris.data'
data_dir='dataset'
train_prefix = 'train'
output_prefix = 'output'
train_path = f"{train_prefix}/{filename}"
s3_train_data = f"s3://{bucket}/{train_path}"
output_location = f's3://{bucket}/{output_prefix}'
print(s3_train_data)
print(output_location)

# 4. Встановлення змінних середовища:
# Встановіть змінні середовища, щоб визначити шляхи та імена файлів.
%env DATA_DIR=$data_dir
%env S3_DATA_BUCKET_NAME = $bucket/$raw_prefix
%env DATASET_NAME = $dataset_name
%env TRAINING_PATH = $bucket/$train_prefix

# 5. Завантаження даних з S3:
# Завантажте набір даних з S3-ковша до робочої директорії за допомогою AWS CLI.
!aws s3 cp s3://$S3_DATA_BUCKET_NAME/$DATASET_NAME ./$DATA_DIR/

# 6. Підготовка даних:
# Завантажте дані в pandas DataFrame та проведіть їх попередній аналіз для розуміння структури та змісту даних.
column_names = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
df = pd.read_csv('./dataset/bezdekIris.data', names=column_names)
df.head()
df.shape
df.info()
df.describe()

# 7. Розділення набору даних:
# Розділіть набір даних на навчальний (X_train та y_train) та тестовий (X_holdout та y_holdout) набори за допомогою функції train_test_split.
numeric_features = list(df.select_dtypes([np.number]).columns)
X = df[numeric_features].copy()
X.drop(columns=['sepal length'], axis=1, inplace=True)
y = df['sepal length']
X_train, X_holdout, y_train, y_holdout = train_test_split(X, y, test_size=0.05)
X_train.shape
X_holdout.shape

# 8. Підготовка даних для Sagemaker:
# Конвертуйте навчальні дані в формат, сумісний з Sagemaker, і завантажте їх у S3.
buf = io.BytesIO()
smac.write_numpy_to_dense_tensor(buf, np.array(X_train).astype('float32'), np.array(y_train).astype('float32'))
buf.seek(0)
boto3.resource('s3').Bucket(bucket).Object(f'{train_path}').upload_fileobj(buf)

# 9. Створення моделі:
# Оберіть контейнер з відповідним алгоритмом (linear-learner) та створіть екземпляр Estimator.
from sagemaker.image_uris import retrieve
container = retrieve('linear-learner', boto3.Session().region_name)
sess = sagemaker.Session()
role = get_execution_role()
linear = sagemaker.estimator.Estimator(container, role, instance_count=1, instance_type='ml.c4.xlarge', output_path=output_location, sagemaker_session=sess)

# 10. Встановлення гіперпараметрів:
# Встановіть гіперпараметри моделі (linear.set_hyperparameters) для навчання моделі.
linear.set_hyperparameters(feature_dim=3, epochs=20, num_models=32, loss='absolute_loss', predictor_type='regressor', mini_batch_size=32, normalize_data=True, normalize_label=False)

# 11. Навчання моделі:
# Запустіть процес навчання моделі (linear.fit), використовуючи дані з S3.
linear.fit({'train': s3_train_data}, job_name=f"job-bezdekIris-{int(time.time())}")

# 12. Розгортання моделі:
# Розгорніть навчальну модель у вигляді ендпоїнту (linear.deploy) для подальшого використання.
linear_predictor = linear.deploy(initial_instance_count=1, instance_type='ml.t2.medium', endpoint_name="bezdekIris-endpoint")

# 13. Прогнозування:
# Виконайте прогнозування на тестовому наборі даних та обрахуйте похибку (RSME).
from sagemaker.deserializers import JSONDeserializer
from sagemaker.serializers import CSVSerializer
linear_predictor.serializer = CSVSerializer()
linear_predictor.deserializer = JSONDeserializer()
result = linear_predictor.predict(X_holdout.values)
predictions = [x['score'] for x in result["predictions"]]
print(f"RSME: {np.sqrt(metrics.mean_squared_error(y_holdout.values, predictions))}")

# 14. Візуалізація:
# Візуалізуйте результати прогнозування за допомогою seaborn та matplotlib.
sns.scatterplot(x=np.array(predictions), y=np.array(y_holdout.values))
sns.regplot(x=np.array(predictions), y=np.array(y_holdout.values))

# 15. Видалення ендпоїнту:
# Видаліть розгорнутий ендпоїнт (sagemaker.Session().delete_endpoint) після завершення роботи.
import sagemaker
sagemaker.Session().delete_endpoint(linear_predictor.endpoint)
