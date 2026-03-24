provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3        = "http://127.0.0.1:4566"
    s3control = "http://127.0.0.1:4566"
    dynamodb  = "http://127.0.0.1:4566"
    sns       = "http://127.0.0.1:4566"
    iam       = "http://127.0.0.1:4566"
    lambda    = "http://127.0.0.1:4566"
    sts       = "http://127.0.0.1:4566"
  }
}

# 1. S3 Bucket
resource "aws_s3_bucket" "image_upload_bucket" {
  bucket = "user-images-bucket"
}

# 2. DynamoDB Table
resource "aws_dynamodb_table" "image_metadata" {
  name         = "ImageMetadata"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ImageId"

  attribute {
    name = "ImageId"
    type = "S"
  }
}

# 3. SNS Topic
resource "aws_sns_topic" "image_proc_topic" {
  name = "image-processing-notifications"
}