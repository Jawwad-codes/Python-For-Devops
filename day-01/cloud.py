import boto3

S3 = boto3.client('s3')
# response = S3.create_bucket(Bucket="python-12345", 
# CreateBucketConfiguration={
#     "LocationConstraint": "ap-south-1"
# })
print("bucket created succesfully")

def upload_to_S3(filename,bucket,object_name):
    response=S3.upload_file(filename,bucket,object_name)
    
    return response

upload_to_S3("E:/Learning Devops 2026/Python For Devops/day-01/api.py", "python-12345", "api.py")

s3= boto3.resource('s3')


for buckets in s3.buckets.all():
    if "frontend" in buckets.name: 
        print(buckets.name)

ec2 = boto3.resource("ec2")
for instance in ec2.instances.all():
    data=instance.id,instance.state, instance.tags
    