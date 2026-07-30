
from app.analyzers.ec2 import EC2Analyzer
from fastapi import APIRouter

router = APIRouter()
@router.get("/scan/ec2")
def scan_ec2():
    analyzer = EC2Analyzer()
    return analyzer.scan()