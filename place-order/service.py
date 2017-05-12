# -*- coding: utf-8 -*-
from datetime import datetime
import boto3
import json
# Get the service resource.

def handler(event, context):
    # Your code goes here!
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Order')
    menu = dynamodb.Table('Menu')
    
    response = menu.get_item(
    Key={
            'menu_id': event['menu_id']
        }
    )  
    item = response['Item']
    s = ''
    i=1
    for val in item['selection']:
        s = s+str(i)+'. '+val+', '
        i= i+1
    s = s[:-2]
    
    time = str(datetime.now().strftime('%m-%d-%Y@%H:%M:%S'))

    table.put_item(
    Item={
            'order_id':event['order_id'],
            'customer_name': event['customer_name'],
            'customer_email': event['customer_email'],
            'menu_id': event['menu_id'],
            'order_status': 'processing',
            'selection' : None,
            'size' : None,
            'cost' : None,
            'order_time' : time
        }
    )
    return {'message' : 'Hi '+event['customer_name']+', please choose one of these selection: '+s}

# if __name__ == "__main__":
#     class Event:
#         def get(self, key):
#             e = {
#                 'order_id' : '1',
#                 'customer_name' : 'John Smith',
#                 'customer_email' : 'foobar@gmail.com'
#             }
#             return e[key]
#     context = 'context'
#     event = Event()
#     print(handler(event, context))