import boto3
import json
import os

# LocalStack'in Lambda içinde sunduğu özel hostname'i alıyoruz
# Eğer bulamazsa (yerel testlerde) 127.0.0.1'e döner
localstack_host = os.environ.get('LOCALSTACK_HOSTNAME', '127.0.0.1')
endpoint_url = f"http://{localstack_host}:4566"

print(f"Bağlanılan Endpoint: {endpoint_url}")

# Servisleri bu dinamik URL ile başlatıyoruz
s3 = boto3.client('s3', endpoint_url=endpoint_url)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
sns = boto3.client('sns', endpoint_url=endpoint_url)

def handler(event, context):
    try:
        # 1. Event içinden S3 bilgilerini çıkar
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        event_time = event['Records'][0]['eventTime']

        print(f"İşleniyor: {file_key} (Bucket: {bucket_name})")

        # 2. DynamoDB'ye kaydet
        table = dynamodb.Table('ImageMetadata')
        table.put_item(
            Item={
                'ImageId': file_key,
                'Bucket': bucket_name,
                'Status': 'PROCESSED',
                'EventTime': event_time
            }
        )

        print(f"Başarıyla kaydedildi: {file_key}")

        return {
            'statusCode': 200,
            'body': json.dumps(f'{file_key} başarıyla işlendi!')
        }
    except Exception as e:
        print(f"HATA OLUŞTU: {str(e)}")
        raise e