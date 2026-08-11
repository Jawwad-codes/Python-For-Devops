from fastapi import FastAPI
from pathlib import Path
import boto3
import sys
# Ensure the parent folder (day-01) is on sys.path so we can import system_utils
sys.path.append(str(Path(__file__).resolve().parents[1]))

from system_utils import system_info

app=FastAPI(title="Devops utilities Api")
@app.get("/hello")
def hello():
    return {"message": "hello i am Jawwad the devops engineer"}
@app.get("/metrics")
def metrics():
    """
     The Api shows the system info like Cpu , Ram and Disk usage
    """
    
    return system_info()


@app.get("/aws/s3")
def getbuckets():
    s3 = boto3.resource('s3')
    buckets=[]
    for bucket in s3.buckets.all():
        buckets.append(bucket.name)
    return buckets


@app.get("/aws/ec2/all")
def get_all_e2():
    ec2 = boto3.resource('ec2')
    instances = []
    for instance in ec2.instances.all():
        instances.append({
            "instance_id": instance.id,
            "state": instance.state,
            "tags": instance.tags,
        })
    return {"instances": instances}
        