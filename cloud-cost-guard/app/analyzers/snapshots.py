from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from app.aws.clients import aws
from app.config import settings
from app.models.recommendation import Recommendation


SNAPSHOT_COST_PER_GB = 0.05 


class SnapshotAnalyzer:

    def scan(self) -> list[Recommendation]:

        findings = []

        snapshots = self._list_snapshots()

        for snapshot in snapshots:
            findings.extend(
                self._analyze_snapshot(snapshot)
            )

        return findings

    def _list_snapshots(self):

        response = aws.ec2.describe_snapshots(
        OwnerIds=["self"]
    )

        return response["Snapshots"]    
    
    def _has_name_tag(tags):

        for tag in tags:
           if tag["Key"] == "Name":
            return True

        return False
    
    def _analyze_snapshot(self, snapshot):
        findings = []
    
        snapshot_id = snapshot["SnapshotId"]
        volume_id = snapshot.get("VolumeId")
        size = snapshot["VolumeSize"]
        start_time = snapshot["StartTime"]
        tags = snapshot.get("Tags", [])
    
        saving = round(size * SNAPSHOT_COST_PER_GB, 2)
    
    
    
        if volume_id:
            try:
                aws.ec2.describe_volumes(VolumeIds=[volume_id])
    
            except ClientError:
            
                findings.append(
                    Recommendation(
                        service="Snapshot",
                        resource_id=snapshot_id,
                        resource_name="Orphaned Snapshot",
                        resource_type="EBS Snapshot",
                        severity="HIGH",
                        issue="Snapshot belongs to a deleted volume",
                        recommendation="Delete this snapshot if it is no longer required.",
                        estimated_monthly_saving_usd=saving,
                        region=settings.aws_region,
                        status="completed",
                    )
                )
    
    
        if start_time < datetime.now(timezone.utc) - timedelta(days=90):
        
            findings.append(
                Recommendation(
                    service="Snapshot",
                    resource_id=snapshot_id,
                    resource_name="Old Snapshot",
                    resource_type="EBS Snapshot",
                    severity="MEDIUM",
                    issue="Snapshot older than 90 days",
                    recommendation="Review and delete this snapshot if it is no longer needed.",
                    estimated_monthly_saving_usd=saving,
                    region=settings.aws_region,
                    status="completed",
                )
            )
    
    
        if not self._has_name_tag(tags):
        
            findings.append(
                Recommendation(
                    service="Snapshot",
                    resource_id=snapshot_id,
                    resource_name="Unnamed Snapshot",
                    resource_type="EBS Snapshot",
                    severity="LOW",
                    issue="Snapshot does not have a Name tag",
                    recommendation="Add a Name tag for easier management.",
                    estimated_monthly_saving_usd=0,
                    region=settings.aws_region,
                    status="completed",
                )
            )
    
        return findings
            
        