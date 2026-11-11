terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 20.0"
  cluster_name    = "prod"
  cluster_version = "1.30"
  subnet_ids      = var.private_subnet_ids
  vpc_id          = var.vpc_id

  eks_managed_node_groups = {
    general = {
      instance_types = ["m6i.large"]
      min_size       = 3
      max_size       = 6
      desired_size   = 3
    }
  }
}

resource "aws_db_instance" "orders" {
  identifier              = "orders-prod"
  engine                  = "postgres"
  engine_version          = "16.3"
  instance_class          = "db.r6g.large"
  allocated_storage       = 200
  multi_az                = false
  backup_retention_period = 1
  skip_final_snapshot     = true
  username                = var.db_user
  password                = var.db_password
}

resource "aws_elasticache_cluster" "sessions" {
  cluster_id      = "sessions-prod"
  engine          = "redis"
  node_type       = "cache.t4g.medium"
  num_cache_nodes = 1
}

resource "aws_sqs_queue" "order_events" {
  name                       = "order-events"
  visibility_timeout_seconds = 30
}
