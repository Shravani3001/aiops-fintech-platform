provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "dvc_storage" {
  bucket = "aiops-fintech-dvc-storage"

  tags = {
    Name = "aiops-fintech-dvc-storage"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.dvc_storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_iam_policy" "dvc_s3_access" {
  name = "dvc-s3-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = "arn:aws:s3:::aiops-fintech-dvc-storage"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "arn:aws:s3:::aiops-fintech-dvc-storage/*"
      }
    ]
  })
}
