import boto3
from app.config import settings


class AWSClient:
    def __init__(self):
        self.ec2 = boto3.client("ec2", region_name=settings.aws_region)
        self.s3 = boto3.client("s3", region_name=settings.aws_region)
        self.logs = boto3.client("logs", region_name=settings.aws_region)
        self.ecr = boto3.client("ecr", region_name=settings.aws_region)
        self.cloudwatch=boto3.client("cloudwatch", region_name=settings.aws_region)
 
aws= AWSClient()        