pipeline {
    agent any

    environment {
        // AWS kimlik bilgilerini LocalStack için 'test' olarak ayarlıyoruz
        AWS_ACCESS_KEY_ID     = 'test'
        AWS_SECRET_ACCESS_KEY = 'test'
        AWS_DEFAULT_REGION    = 'us-east-1'
    }

    stages {
        stage('🚀 Checkout') {
            steps {
                // Kodlarını GitHub'dan çeker
                checkout scm
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

        stage('🧪 Automated Test') {
    steps {
        script {
            echo "Testing S3 connectivity..."
            // Jenkins içinden LocalStack S3'e dosya yükleme denemesi
            // Not: Altyapıda kullandığımız 172.17.0.1 IP'sini burada da kullanıyoruz.
            sh """
                aws --endpoint-url=http://172.17.0.1:4566 s3 cp ../src/asd.jpg s3://user-images-bucket/test-check.jpg
                aws --endpoint-url=http://172.17.0.1:4566 s3 ls s3://user-images-bucket/
            """
        }
    }
}

        stage('✅ Test Connection') {
            steps {
                // Jenkins konteyneri içinden LocalStack'e erişim testi
                // Docker Desktop sayesinde 'host.docker.internal' Mac'indeki LocalStack'i görür
                sh 'aws --endpoint-url=http://host.docker.internal:4566 s3 ls'
                sh 'aws --version || (apt-get update && apt-get install -y awscli)'
            }
        }
    }
}