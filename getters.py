import boto3

TABLE_NAME = 'BluetoothSignals'
PRIMARY_COLUMN_NAME = 'location'
COLUMNS = ['signals_num', 'max', 'min']

CLIENT = boto3.client('dynamodb')

DB = boto3.resource('dynamodb')
TABLE = DB.Table(TABLE_NAME)

def get_location():
    response = TABLE.get_item(
        Key={
            PRIMARY_COLUMN_NAME: 'Mhome'
        }
    )
    return response['Item']

def get_max():
    data = get_location()
    return data['max']

def get_min():
    data = get_location()
    return data['min']
