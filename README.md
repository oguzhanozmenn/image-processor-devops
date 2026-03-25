# 🏗️ Enterprise Image Processing Pipeline (Serverless & IaC)

Bu proje, modern bulut mimarilerinde kullanılan **Event-Driven (Olay Güdümlü)** ve **Decoupled (Ayrık)** tasarım desenlerini kullanarak oluşturulmuş kurumsal bir imaj işleme hattıdır.

## 🚀 Mimari Özellikler
- **Infrastructure as Code (IaC):** Tüm altyapı Terraform ile yönetilmektedir.
- **CI/CD:** Jenkins üzerinden otomatik test ve dağıtım (Terraform Apply) süreçleri yönetilir.
- **Asenkron Mesajlaşma:** S3 ve Lambda arasında **AWS SQS** kullanılarak yüksek ölçeklenebilirlik sağlanmıştır.
- **Hata Yönetimi:** İşlenemeyen mesajlar için **Dead Letter Queue (DLQ)** mekanizması kurulmuştur.
- **NoSQL Veritabanı:** İşlem meta verileri **DynamoDB** üzerinde saklanmaktadır.

## 🛠️ Teknolojiler
- **Cloud Simulation:** LocalStack
- **IaC:** Terraform
- **CI/CD:** Jenkins
- **Language:** Python 3.9 (Boto3)
- **AWS Services:** S3, SQS, Lambda, DynamoDB, IAM

## 📋 Nasıl Çalışır?
1. Kullanıcı S3 kovasına bir resim yükler.
2. S3, yükleme olayını SQS kuyruğuna bir mesaj olarak bırakır.
3. AWS Lambda, kuyruktaki mesajı alır, dosya tipi kontrolünü yapar.
4. Sonuçlar (Başarılı/Reddedildi) DynamoDB tablosuna yazılır.