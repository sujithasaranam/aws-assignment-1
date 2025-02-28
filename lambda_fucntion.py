import boto3
import json
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('erp-orders')
QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/980921744378/erp-orders-queue"
sqs = boto3.client('sqs', region_name='ap-south-1')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        records = event['Records']
        for record in records:
            message_body = json.loads(record['body'])
            if "order_id" not in message_body:
                raise Exception("Message does not contain order_id, not a valid record.")
            logger.info(f"Message Processed: {message_body}")
            table.put_item(Item=message_body)
            logger.info(f"Stored item with order_id: {message_body['order_id']} in dynamoDB")
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=record['receiptHandle'])
            logger.info(f"Message deleted from SQS: {message_body}")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise e
