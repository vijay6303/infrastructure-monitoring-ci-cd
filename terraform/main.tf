terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "infrastructure_info" {
  filename = "${path.module}/generated/infrastructure-info.txt"

  content = <<-EOT
    Infrastructure Monitoring Project
    Provisioned using Terraform

    Environment: Ubuntu on WSL2
    Purpose: DevOps Infrastructure Automation
  EOT

  file_permission = "0644"
}

output "created_file" {
  value = local_file.infrastructure_info.filename
}
