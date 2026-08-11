from app.aws.clients import aws
from app.config import settings
from app.models.recommendation import Recommendation
from app.models.recommendation import ScanResult


EBS_STORAGE_COST_PER_GB = 0.08


class EBSAnalyzer:

    def __init__(self):
        self.cost_service = CostService()

    def scan(self):
        findings = []
        actual_cost = self.cost_service.get_service_cost("Amazon Elastic Block Store")

        volumes = self._list_volumes()

        for volume in volumes:

            findings.extend(self._analyze_volume(volume))

        return ScanResult(
            service="EBS",
            actual_monthly_cost_usd=actual_cost,  # Placeholder, replace with actual cost if available
            findings=findings
        )

    def _list_volumes(self):
        response = aws.ec2.describe_volumes()
        return response["Volumes"]

    def _analyze_volume(self, volume):

        findings = []

        volume_id = volume["VolumeId"]
        volume_type = volume["VolumeType"]
        size = volume["Size"]
        state = volume["State"]

        attachments = volume["Attachments"]

        monthly_cost = round(size * EBS_STORAGE_COST_PER_GB, 2)

   

        if not attachments:

            findings.append(
                Recommendation(
                    service="EBS",
                    resource_id=volume_id,
                    resource_name="Unattached Volume",
                    resource_type=volume_type,
                    severity="HIGH",
                    issue="Unattached EBS Volume",
                    recommendation="Delete this volume if it is no longer required.",
                    estimated_monthly_saving_usd=monthly_cost,
                    actual_cost_usd=actual_cost,
                    region=settings.aws_region,
                    status=state,
                )
            )

            return findings


        instance_id = attachments[0]["InstanceId"]

        try:

            response = aws.ec2.describe_instances(
                InstanceIds=[instance_id]
            )

            instance = response["Reservations"][0]["Instances"][0]

            instance_state = instance["State"]["Name"]

            if instance_state == "stopped":

                findings.append(
                    Recommendation(
                        service="EBS",
                        resource_id=volume_id,
                        resource_name=f"Volume attached to {instance_id}",
                        resource_type=volume_type,
                        severity="MEDIUM",
                        issue="Volume attached to stopped EC2 instance",
                        recommendation="Review whether the stopped instance and its volume are still required.",
                        estimated_monthly_saving_usd=monthly_cost,
                        actual_cost_usd=actual_cost,
                        region=settings.aws_region,
                        status=state,
                    )
                )

        except Exception:
            pass



        if volume_type == "gp2":

            findings.append(
                Recommendation(
                    service="EBS",
                    resource_id=volume_id,
                    resource_name="Legacy gp2 Volume",
                    resource_type=volume_type,
                    severity="LOW",
                    issue="gp2 volume detected",
                    recommendation="Consider migrating this volume to gp3 for better price-performance.",
                    estimated_monthly_saving_usd=round(monthly_cost * 0.20, 2),
                    aws_cost_usd=actual_cost,
                    region=settings.aws_region,
                    status=state,
                )
            )

        return findings