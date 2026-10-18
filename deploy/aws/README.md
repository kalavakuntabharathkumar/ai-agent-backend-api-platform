# AWS deployment guide
Suggested route: build the image, push to Amazon ECR, deploy to ECS Fargate behind an Application Load Balancer. Use CloudWatch logs/metrics and Secrets Manager. Configure `/health` and `/ready` probes. This is a guide, not evidence of a live deployment. Add RDS/PostgreSQL, IAM least privilege, autoscaling, and security/load tests.
