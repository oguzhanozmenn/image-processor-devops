provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true

  # Tüm servisleri LocalStack'e yönlendiriyoruz
  endpoints {
    s3       = "http://localhost:4566"
    lambda   = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    sns      = "http://localhost:4566"
    iam      = "http://localhost:4566"
  }
}

# 1. S3 Bucket: Resimlerin yükleneceği yer
resource "aws_s3_bucket" "image_upload_bucket" {
  bucket = "user-images-bucket"
}

# 2. DynamoDB: Resim bilgilerinin tutulacağı tablo
resource "aws_dynamodb_table" "image_metadata" {
  name           = "ImageMetadata"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ImageId"

  attribute {
    name = "ImageId"
    type = "S"
  }
}

# 3. SNS Topic: Bildirim kanalı
resource "aws_sns_topic" "image_proc_topic" {
  name = "image-processing-notifications"
}