import boto3
import json
import os

# AWS Servis istemcilerini hazırlıyoruz
# Not: LocalStack ortamında olduğumuz için endpoint_url belirtiyoruz
s3 = boto3.client('s3', endpoint_url="http://127.0.0.1:4566")
dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566")
sns = boto3.client('sns', endpoint_url="http://127.0.0.1:4566")


def handler(event, context):
    # 1. Event içinden S3 bilgilerini çıkar (Hangi bucket, hangi dosya?)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    print(f"Yeni resim algılandı: {file_key} (Bucket: {bucket_name})")

    # 2. DynamoDB'ye kaydet (Metadata)
    table = dynamodb.Table('ImageMetadata')
    table.put_item(
        Item={
            'ImageId': file_key,
            'Bucket': bucket_name,
            'Status': 'PROCESSED',
            'EventTime': event['Records'][0]['eventTime']
        }
    )

    # 3. SNS ile Bildirim Gönder (Basit bir log mesajı gibi)
    # SNS ARN'sini Terraform'dan alacağız ama şimdilik log basalım
    print(f"DynamoDB kaydı başarılı: {file_key}")

    return {
        'statusCode': 200,
        'body': json.dumps('İşlem Başarılı!')
    }