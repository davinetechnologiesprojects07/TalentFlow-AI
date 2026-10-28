variable "aws_region" {
  type    = string
  default = "us-east-1" # Change to your preferred region
}

variable "ami_id" {
  type        = string
  description = "The AMI ID for the EC2 instance (e.g., Ubuntu 22.04 or Amazon Linux 2)"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (Free tier eligible)"
  default     = "t2.micro" # Use "t3.micro" if your region doesn't support t2.micro
}