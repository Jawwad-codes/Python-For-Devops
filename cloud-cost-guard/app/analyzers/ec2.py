from datetime import datetime, timedelta, timezone

from app.aws.clients import aws
from app.config import INSTANCE_MONTHLY_COST
from app.models.recommendation import Recommendation
from app.services.cost_service import CostService
from app.models.recommendation import ScanResult



class EC2Analyzer:
    def __init__(self):
        self.cost_service = CostService()
    def scan(self):
        findings = []
        actual_cost = self.cost_service.get_service_cost("Amazon Elastic Compute Cloud - Compute")

        response = aws.ec2.describe_instances()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:

                if instance["State"]["Name"] != "running":
                    continue

                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                name = self._get_instance_name(instance.get("Tags", []))
                availability_zone = instance["Placement"]["AvailabilityZone"]
                launch_time = instance["LaunchTime"]

                avg_cpu = self._get_average_cpu(instance_id)
                print(avg_cpu)

                findings.append(
                    self._build_recommendation(
                        instance_id=instance_id,
                        name=name,
                        instance_type=instance_type,
                        availability_zone=availability_zone,
                        launch_time=launch_time,
                        avg_cpu=avg_cpu,
                        status=instance["State"]["Name"],
                    )
                )

        return ScanResult(
            service="EC2",
            actual_monthly_cost_usd=actual_cost,
            findings=findings
        )

    def _get_instance_name(self, tags):
        for tag in tags:
            if tag["Key"] == "Name":
                return tag["Value"]

        return "Unnamed"

    def _get_average_cpu(self, instance_id):
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=7)

        response = aws.cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id,
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Average"],
        )

        datapoints = response["Datapoints"]

        if not datapoints:
            return 0

        total = sum(point["Average"] for point in datapoints)

        return round(total / len(datapoints), 2)

    def _build_recommendation(
        self,
        instance_id,
        name,
        instance_type,
        availability_zone,
        launch_time,
        avg_cpu,
        status,
        actual_cost
    ):

        if avg_cpu < 5:
            severity = "HIGH"
            issue = "Idle EC2 Instance"
            recommendation = "Consider stopping or downsizing this instance."
        elif avg_cpu < 15:
            severity = "MEDIUM"
            issue = "Low Utilization"
            recommendation = "Review instance utilization."
        else:
            severity = "LOW"
            issue = "Healthy"
            recommendation = "No action required."
            
        return Recommendation(
            service="EC2",
            resource_id=instance_id,
            resource_name=name,
            resource_type=instance_type,
            severity=severity,
            issue=issue,
            recommendation=recommendation,
            estimated_monthly_saving_usd=INSTANCE_MONTHLY_COST.get(instance_type, 0),
            actual_cost_usd=actual_cost,
            region=availability_zone[:-1],
            status=status,
)    