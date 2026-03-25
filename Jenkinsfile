pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = 'test'
        AWS_SECRET_ACCESS_KEY = 'test'
        AWS_DEFAULT_REGION    = 'us-east-1'
        TF_HTTP_RETRY_MAX     = '10'
        TF_HTTP_TIMEOUT       = '300'
    }

    stages {
        stage('🚀 Checkout & CLI Check') {
            steps {
                checkout scm
                sh 'aws --version || (apt-get update && apt-get install -y awscli)'
            }
        }

        stage('🛠️ Terraform Init') {
            steps {
                dir('infra') {
                    sh 'terraform init'
                }
            }
        }

        stage('🌍 Terraform Apply') {
            steps {
                dir('infra') {
                    sh 'terraform apply --auto-approve'
                }
            }
        }

        stage('🧪 Automated Smoke Test') {
            steps {
                script {
                    echo "S3 Bağlantısı Test Ediliyor..."
                    sh "aws --endpoint-url http://host.docker.internal:4566 s3 cp asd.jpg s3://user-images-bucket/test-check.jpg"
                    sh "aws --endpoint-url http://host.docker.internal:4566 s3 ls s3://user-images-bucket/"
                }
            }
        }

       stage('🔍 Verify Enterprise Pipeline') {
            steps {
                script {
                    echo "SQS ve Lambda orkestrasyonu bekleniyor..."
                    sh 'sleep 10' // Mesajın kuyruktan geçmesi için süre ver
                    echo "Sonuçlar DynamoDB'den okunuyor:"
                    sh "aws --endpoint-url http://host.docker.internal:4566 dynamodb scan --table-name ImageMetadata"

                    echo "SQS Kuyruk Durumu Kontrol Ediliyor:"
                    sh "aws --endpoint-url http://host.docker.internal:4566 sqs get-queue-attributes --queue-url http://host.docker.internal:4566/000000000000/image-processing-queue --attribute-names All"
                }
            }
        }
    } // stages burada bitiyor

    // POST bloğu BURADA, yani pipeline parantezinin içinde olmalı
    post {
        always {
            echo "Pipeline tamamlandı, temizlik yapılabilir."
        }
        success {
            echo "✅ Harika! Tüm sistem doğrulandı."
        }
    }
} // pipeline burada bitiyor