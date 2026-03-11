output "dvc_policy_arn" {
  value = aws_iam_policy.dvc_s3_access.arn
}

output "dvc_bucket_name" {
  value = aws_s3_bucket.dvc_storage.bucket
}