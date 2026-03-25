import json
import boto3
import os

# LocalStack için endpoint ayarı (Lambda içinde genellikle gerekmez ama debug için iyidir)
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    # 1. Olayı yakala (S3'ten gelen veri)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    print(f"🚀 Yeni dosya algılandı: {file_key} (Bucket: {bucket_name})")

    try:
        # 2. Dosya bilgilerini al (Metadata)
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        file_size = response['ContentLength']
        file_type = response['ContentType']

        # 3. DynamoDB'ye kaydet
        table = dynamodb.Table('ImageMetadata')
        table.put_item(
            Item={
                'ImageID': file_key,
                'Size': file_size,
                'Type': file_type,
                'Status': 'PROCESSED'
            }
        )

        print(f"✅ {file_key} başarıyla işlendi ve DB'ye kaydedildi. Boyut: {file_size} bytes")

        return {
            'statusCode': 200,
            'body': json.dumps('İşlem Başarılı!')
        }

    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        raise e