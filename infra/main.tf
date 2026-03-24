provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3       = "http://host.docker.internal:4566"
    dynamodb = "http://host.docker.internal:4566"
    lambda   = "http://host.docker.internal:4566"
    iam      = "http://host.docker.internal:4566"
    sns      = "http://host.docker.internal:4566"
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
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../src/handler.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "image_processor" {
  filename      = "lambda_function_payload.zip"
  function_name = "image-processor-handler"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "handler.handler" # dosyaadı.fonksiyonadı
  runtime       = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.image_upload_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.image_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

# Lambda'ya S3'ten tetiklenme izni ver
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.image_upload_bucket.arn
}