from botocore.exceptions import ClientError
from app.aws.clients import aws
from app.config import settings
from app.models.recommendation import Recommendation

ELASTIC_IP_MONTHLY_COST = 0.005

class ElasticIPAnalyzer:

    def scan(self) -> list[Recommendation]:
        findings = []

        elastic_ips = self._list_elastic_ips()

        for elastic_ip in elastic_ips:
            findings.extend(
                self._analyze_elastic_ip(elastic_ip)
            )

        return findings

    def _list_elastic_ips(self):
        response = aws.ec2.describe_addresses()
        return response["Addresses"]

    def _analyze_elastic_ip(self, elastic_ip):
        findings = []

        allocation_id = elastic_ip.get("AllocationId")
        public_ip = elastic_ip.get("PublicIp")
        instance_id = elastic_ip.get("InstanceId")

        if "AssociationId" not in elastic_ip:
            findings.append(
                Recommendation(
                    service="Elastic IP",
                    resource_id=allocation_id,
                    resource_name=public_ip,
                    resource_type="Elastic IP",
                    severity="HIGH",
                    issue="Unassociated Elastic IP",
                    recommendation="Release this Elastic IP if it is no longer required.",
                    estimated_monthly_saving_usd=ELASTIC_IP_MONTHLY_COST,
                    region=settings.aws_region,
                    status="unassociated",
                )
            )

            return findings
        if not instance_id:
            return findings
        try:
            response=aws.ec2.describe_instances(InstanceIds=[instance_id])
            instances=response["Reservations"][0]["Instances"]
            if instances["State"]["Name"] == "stopped":
                findings.append(
                    Recommendation(
                        service="Elastic IP",
                        resource_id=allocation_id,
                        resource_name=public_ip,
                        resource_type="Elastic IP",
                        severity="MEDIUM",
                        issue="Elastic IP associated with a stopped instance",
                        recommendation="Release this Elastic IP if it is no longer required.",
                        estimated_monthly_saving_usd=ELASTIC_IP_MONTHLY_COST,
                        region=settings.aws_region,
                        status="associated with stopped instance",
                    )
                )
        except ClientError:
            pass
    