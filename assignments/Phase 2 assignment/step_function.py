"""imports needed to run code"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

QUEUE_URL = os.getenv('STEP_FUNCTION_QUEUE')
STEP_FUNCTION_ARN = os.getenv('STEP_FUNCTION_URL')

sqs_client = boto3.client('sqs', region_name='ap-south-1')
sfn_client = boto3.client('stepfunctions', region_name='ap-south-1')


def send_order_to_sqs(message):
    """ sends message to sqs """
    result = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    return result


def trigger_step_function(sqs_message):
    """Triggers AWS Step Function execution"""
    step_fucntion_result = sfn_client.start_execution(
        stateMachineArn=STEP_FUNCTION_ARN,
        input=json.dumps(sqs_message)
    )
    return step_fucntion_result


if __name__ == "__main__":
    date_time = datetime.isoformat(datetime.now())
    orders = [{'order_id':'11', 'customer_name': 'alice',
            'product_name': 'pen', 'quantity': 2, 'price': 50, 'order_date': date_time}
              ]
    for order in orders:
        response = send_order_to_sqs(order)
        print(f"Sent order {order}")

        step_response = trigger_step_function(order)
        print(f"Triggered Step Function for order {order}")
