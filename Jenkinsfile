pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = 'test'
        AWS_SECRET_ACCESS_KEY = 'test'
        AWS_DEFAULT_REGION    = 'us-east-1'
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
                    echo "S3 Bağlantısı Test Ediliyor (host.docker.internal üzerinden)..."
                    sh "aws --endpoint-url http://host.docker.internal:4566 s3 cp asd.jpg s3://user-images-bucket/test-check.jpg"
                    sh "aws --endpoint-url http://host.docker.internal:4566 s3 ls s3://user-images-bucket/"
                }
            }
        }
        stage('🔍 Verify Database') {
            steps {
                script {
                    echo "DynamoDB kayıtları kontrol ediliyor..."
                    // Lambda'nın çalışması için 5 saniye bekle
                    sh 'sleep 5'
                    // Kaydı sorgula
                    sh "aws --endpoint-url http://host.docker.internal:4566 dynamodb scan --table-name ImageMetadata"
                }
            }
        }
    }
}
post {
        always {
            echo "Pipeline tamamlandı, temizlik yapılabilir."
            // İstersen buraya terraform destroy ekleyebiliriz ama
            // şimdilik sonuçları görmen için manuel bırakalım.
        }
    }