# Machine Learning in AWS Sagemaker: приклад на наборі даних bezdekIris

Цей проект демонструє основні елементи машинного навчання з використанням AWS Sagemaker на прикладі роботи з набором даних **bezdekIris**. Проект містить операції з підготовки даних, навчання моделі та прогнозування з використанням Sagemaker.

## Вимоги

- [AWS CLI](https://aws.amazon.com/cli/)
- [Sagemaker SDK](https://sagemaker.readthedocs.io/en/stable/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

## Виконання

### Підготовка даних

- Скопіюйте дані з S3-ковша у вашу робочу директорію:

    ```bash
    aws s3 cp s3://$S3_DATA_BUCKET_NAME/$DATASET_NAME ./$DATA_DIR/
    ```

- Завантажте дані та проведіть їх попередній аналіз:

    ```python
    column_names = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
    df = pd.read_csv('./dataset/bezdekIris.data', names=column_names)
    print(df.head())
    ```

### Навчання моделі

- Розділіть набір даних на навчальний і тестовий набори:

    ```python
    X_train, X_holdout, y_train, y_holdout = train_test_split(df.drop(columns=['class']), df['class'], test_size=0.05)
    ```

- Навчіть модель у Sagemaker:

    ```python
    linear.set_hyperparameters(
        feature_dim=3,
        epochs=20,
        num_models=32,
        loss='absolute_loss',
        predictor_type='regressor',
        mini_batch_size=32,
        normalize_data=True,
        normalize_label=False
    )
    linear.fit({'train': s3_train_data}, job_name=f"job-bezdekIris-{int(time.time())}")
    ```

### Прогнозування

- Виконайте прогнозування на тестовому наборі:

    ```python
    result = linear_predictor.predict(X_holdout.values)
    predictions = [x['score'] for x in result['predictions']]
    print(f"RSME: {np.sqrt(metrics.mean_squared_error(y_holdout.values, predictions))}")
    ```

- Візуалізуйте результати:

    ```python
    sns.scatterplot(x=predictions, y=y_holdout.values)
    sns.regplot(x=predictions, y=y_holdout.values)
    plt.show()
    ```

### Видалення ресурсів

- Видаліть створений ендпоїнт після завершення роботи:

    ```python
    sagemaker.Session().delete_endpoint(linear_predictor.endpoint)
    ```

## Ліцензія

Цей проект доступний під ліцензією [MIT](LICENSE).
