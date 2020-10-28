try:
    import os
    from script import *
    import sys
    import datetime
    import time
    import boto3
    import threading
    from getters import *
except Exception as e:
    print('Error importing in send_data.py: {}'.format(e))

LOCATION = 'Mhome'
TABLE_NAME = 'BluetoothSignals'

class MyDb():
    def __init__(self):
        self.Table_Name = TABLE_NAME
        self.db = boto3.resource('dynamodb', region_name='us-west-1')
        self.table = self.db.Table(TABLE_NAME)
        self.client = boto3.client('dynamodb')

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'location' : LOCATION
            }
        )

        return response['Item']

    def put(self, location='', num='', maxi='', mini=''):
        self.table.put_item(
            Item={
                'location': location,
                'signals_num': num,
                'min': mini,
                'max': maxi
            }
        )

    def delete(self, location=''):
        self.client.delete_item(
            Key={
                'location': location
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName=TABLE_NAME
        )

        return response

    @staticmethod
    def signals():
        pi_num = run_scan()
        if pi_num == 0:
            print('Error of some kind, or there are no signals in this area')
        else:
            print('Signal for {} is {}'.format(LOCATION, pi_num))

        return pi_num


def get_max_min(maxi, mini, num):
    if num < mini and mini != 0:
        mini = num
    elif num > maxi:
        maxi = num

    return str(maxi), str(mini)



def main():
    threading.Timer(interval=10, function=main).start()
    obj = MyDb()

    pi_num = obj.signals()

    maxi, mini = get_max_min(int(get_max()), int(get_min()), pi_num)
    obj.put(location=LOCATION, num=str(pi_num), maxi=str(maxi), mini=str(mini))

    print('Uploaded to cloud location: {}, Number of Signals {}'.format(LOCATION, pi_num))

if __name__ == '__main__':
    main()
