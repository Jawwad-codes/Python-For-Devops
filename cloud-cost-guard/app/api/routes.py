
from app.analyzers.ec2 import EC2Analyzer 
from app.analyzers.ebs import EBSAnalyzer
from app.analyzers.snapshots import SnapshotAnalyzer
from fastapi import APIRouter

router = APIRouter()

@router.get("/scan/ec2")
def scan_ec2():
    analyzer = EC2Analyzer()
    return analyzer.scan()

@router.get("/scan/ebs")
def scan_ebs():    
    analyzer = EBSAnalyzer()
    return analyzer.scan()

@router.get("/scan/snapshots")
def scan_snapshots():
    analyzer=SnapshotAnalyzer()
    return analyzer.scan()