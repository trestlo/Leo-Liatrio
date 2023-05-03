output "ecr_url" {
  value = aws_ecr_repository.ecr_repository.repository_url
}

output "cluster_name" {
  value = var.cluster_name
}
