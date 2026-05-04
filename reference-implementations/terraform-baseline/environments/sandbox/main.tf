module "vpc" {
  source      = "../../modules/vpc"
  environment = "sandbox"
  region      = "asia-south1"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
