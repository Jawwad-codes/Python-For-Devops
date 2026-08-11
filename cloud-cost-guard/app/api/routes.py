
from app.analyzers.ec2 import EC2Analyzer 
from app.analyzers.ebs import EBSAnalyzer
from app.analyzers.snapshots import SnapshotAnalyzer
from app.analyzers.eip import ElasticIPAnalyzer
from fastapi import APIRouter
router = APIRouter()

@router.get("/scan/ec2")
def scan_ec2():
    """
    Scan EC2 instances for cost optimization opportunities.
    
    """
    
    analyzer = EC2Analyzer()
    return analyzer.scan()

@router.get("/scan/ebs")
def scan_ebs():    
    """
    Scan EBS volumes for cost optimization opportunities.
    """
    analyzer = EBSAnalyzer()
    return analyzer.scan()

@router.get("/scan/snapshots")
def scan_snapshots():
    """
    Scan snapshots for cost optimization opportunities.
    """
    analyzer=SnapshotAnalyzer()
    return analyzer.scan()

@router.get("/scan/eip")
def scan_eip():
    """
    Scan Elastic IPs for cost optimization opportunities.
    """
    analyzer=ElasticIPAnalyzer()
    return analyzer.scan()

from app.analyzers.ecr import ECRAnalyzer


@router.get("/scan/ecr")
def scan_ecr():
    """
    Scan ECR repositories for cost optimization opportunities.
    """

    analyzer = ECRAnalyzer()

    return analyzer.scan()    