# -*- coding: utf-8 -*-
import boto3
import json

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    order = dynamodb.Table('Order')
    menu = dynamodb.Table('Menu')

    orderVal = order.get_item(
    Key={
            'order_id': event['order_id']
        }
    )  
    orderItem=orderVal['Item']

    menuVal = menu.get_item(
    Key={
            'menu_id': orderItem['menu_id']
        }
    )
    menuItem=menuVal['Item'] 

    if orderItem['selection'] is None:
        if int(event['input']) > len(menuItem['selection']) or int(event['input']) < 1:
            return {'message' : 'please enter valid input within selection range'}
        else:
            response = order.update_item(
                Key={
                    'order_id': event['order_id']
                },
                UpdateExpression='SET selection = :val',
                ExpressionAttributeValues={
                    ':val': menuItem['selection'][int(event['input'])-1]
                },
                ReturnValues="NONE"
            )
            s = ''
            i=1
            for val in menuItem['size']:
                s = s+str(i)+'. '+val+', '
                i= i+1
            s = s[:-2]
            return {'message' : 'Which size do you want? '+s}
    else:
        if int(event['input']) > len(menuItem['size']) or int(event['input']) < 1:
            return {'message' : 'please enter valid input within size range'}
        else:
            price = menuItem['price'][int(event['input'])-1]
            response = order.update_item(
                Key={
                    'order_id': event['order_id']
                },
                UpdateExpression='SET size = :val1, cost = :val2',
                ExpressionAttributeValues={
                    ':val1' : menuItem['size'][int(event['input'])-1],
                    ':val2' : price
                },
                ReturnValues="NONE"
            )
            return {'message' : 'Your order costs $'+str(price)+'. We will email you when the order is ready. Thank you!'}
