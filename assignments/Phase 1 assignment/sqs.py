"""imports needed to run code"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

QUEUE_URL = os.getenv('QUEUE_URL')

sqs_client = boto3.client('sqs', region_name='ap-south-1')


def send_order_to_sqs(message):
    """ sends message to sqs """
    result = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    return result


if __name__ == "__main__":
    date_time = datetime.isoformat(datetime.now())
    orders = ["hi", "hello"]
    # orders = [{'order_id': '6', 'customer_name': 'sujitha',
    #         'product_name': 'pen', 'quantity': 2, 'price': 50, 'order_date': date_time},
    #           {'order_id': '7', 'customer_name': 'praneetha',
    #            'product_name': 'pencil', 'quantity': 10, 'price': 50, 'order_date': date_time},
    #           {'order_id': '8', 'customer_name': 'latha',
    #            'product_name': 'box', 'quantity': 3, 'price': 100, 'order_date': date_time},
    #           {'order_id': '9', 'customer_name': 'chandu',
    #            'product_name': 'bottle', 'quantity': 9, 'price': 450, 'order_date': date_time},
    #           {'order_id': '10', 'customer_name': 'dileep',
    #            'product_name': 'cap', 'quantity': 3, 'price': 150, 'order_date': date_time},
    #           ]
    for order in orders:
        response = send_order_to_sqs(order)
        print(f"Sent order {order}")
