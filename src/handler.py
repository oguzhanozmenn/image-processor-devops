import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    allowed_extensions = ['.jpg', '.jpeg', '.png']

    for record in event['Records']:
        try:
            sqs_body = json.loads(record['body'])
            if 'Records' not in sqs_body: continue

            s3_event = sqs_body['Records'][0]
            bucket_name = s3_event['s3']['bucket']['name']
            file_key = urllib.parse.unquote_plus(s3_event['s3']['object']['key'])

            # GÜVENLİK KONTROLÜ: Uzantı kontrolü
            extension = "." + file_key.split('.')[-1].lower()

            if extension not in allowed_extensions:
                print(f"⚠️ GÜVENLİK UYARISI: Geçersiz dosya tipi ({extension}). İşlem iptal edildi.")
                status = "REJECTED_INVALID_TYPE"
            else:
                print(f"🚀 İşleniyor: {file_key}")
                status = "PROCESSED_SUCCESSFULLY"

            # DynamoDB Kaydı
            table = dynamodb.Table('ImageMetadata')
            table.put_item(
                Item={
                    'ImageID': file_key,
                    'Status': status,
                    'Extension': extension,
                    'Infrastructure': 'Enterprise-SQS-Lambda',
                    'Timestamp': s3_event['eventTime']
                }
            )

        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            raise e

    return {'statusCode': 200, 'body': 'Pipeline Completed'}