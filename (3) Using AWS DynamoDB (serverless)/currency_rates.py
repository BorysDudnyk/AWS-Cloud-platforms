import boto3
from decimal import Decimal  
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CurrencyRates:
    """Encapsulates an Amazon DynamoDB table of currency exchange rates."""

    def __init__(self, dyn_resource, table_name):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        :param table_name: The name of the DynamoDB table.
        """
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table(table_name)

    def create_table(self, table_name):
        """Create a DynamoDB table."""
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "r030", "KeyType": "HASH"},
                    {"AttributeName": "txt", "KeyType": "RANGE"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "r030", "AttributeType": "N"},
                    {"AttributeName": "txt", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10
                }
            )
            self.table.wait_until_exists()
        except Exception as e:
            logger.error("Couldn't create table %s. Error: %s", table_name, e)
            raise

    def add_rate(self, r030, txt, rate, c, exchange_date):
        """Add a currency exchange rate to the table."""
        try:
            self.table.put_item(
                Item={
                    "r030": r030,
                    "txt": txt,
                    "rate": Decimal(str(rate)),  # Використано Decimal для конвертації рейту в строку
                    "c": c,
                    "exchange_date": exchange_date
                }
            )
        except Exception as e:
            logger.error("Couldn't add rate %s. Error: %s", txt, e)
            raise

    def delete_rate(self, r030, txt):
        """Delete a currency exchange rate from the table."""
        try:
            self.table.delete_item(
                Key={"r030": r030, "txt": txt}
            )
        except Exception as e:
            logger.error("Couldn't delete rate %s. Error: %s", txt, e)
            raise

    def get_rate(self, r030, txt):
        """Get currency exchange rate from the table."""
        try:
            response = self.table.get_item(
                Key={"r030": r030, "txt": txt}
            )
            return response.get("Item", None)
        except Exception as e:
            logger.error("Couldn't get rate %s. Error: %s", txt, e)
            raise

def main():
    # Connect to DynamoDB
    region = input("Enter the region: ")  # Введення регіону
    access_key_id = input("Enter your Access Key ID: ")  # Введення ключа айді
    secret_access_key = input("Enter your Secret Access Key: ")  # Введення секретного ключа
    session_token = input("Enter your Session Token (optional): ")  # Введення токену сесії (опціонально)

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token if session_token else None
    )

    # Create instance of CurrencyRates class
    rates_table_name = input("Enter the table name: ")  # Введення імені таблиці
    rates = CurrencyRates(dynamodb, rates_table_name)

    # Main loop
    while True:
        print("\n1. Add currency rate")
        print("2. Delete currency rate")
        print("3. Get currency rate")
        print("4. Exit")  
        choice = input("Enter your choice: ")

        if choice == "1":
            r030 = int(input("Enter r030: "))
            txt = input("Enter txt: ")
            rate = float(input("Enter rate: "))
            c = input("Enter c: ")
            exchange_date = input("Enter exchange date (YYYY-MM-DD): ")
            rates.add_rate(r030, txt, rate, c, exchange_date)
            print("Currency rate added successfully.")

        elif choice == "2":
            r030 = int(input("Enter r030: "))
            txt = input("Enter txt: ")
            rates.delete_rate(r030, txt)
            print("Currency rate deleted successfully.")

        elif choice == "3":
            r030 = int(input("Enter r030: "))
            txt = input("Enter txt: ")
            rate = rates.get_rate(r030, txt)
            if rate:
                print("Currency rate:", rate["rate"])
                print("Exchange date:", rate["exchange_date"])
            else:
                print("Currency rate not found.")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
