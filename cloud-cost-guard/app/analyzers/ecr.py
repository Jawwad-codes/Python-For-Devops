from datetime import datetime, timedelta, timezone

from app.aws.clients import aws
from app.models.recommendation import Recommendation


class ECRAnalyzer:

    def scan(self):
        findings = []

        repositories = aws.ecr.describe_repositories()["repositories"]

        for repository in repositories:

            repository_name = repository["repositoryName"]

            images = self._get_images(repository_name)

            for image in images:

                findings.append(
                    self._build_recommendation(
                        repository_name=repository_name,
                        image=image,
                    )
                )

        return findings

    def _get_images(self, repository_name):

        response = aws.ecr.describe_images(
            repositoryName=repository_name
        )

        return response["imageDetails"]

    def _build_recommendation(self, repository_name, image):

        image_digest = image["imageDigest"]
        image_size = image.get("imageSizeInBytes", 0)
        pushed_at = image.get("imagePushedAt")

        tags = image.get("imageTags", [])

        # Untagged image
        if not tags:

            severity = "HIGH"
            issue = "Untagged ECR Image"
            recommendation = (
                "Delete this untagged image if it is no longer required."
            )

        # Old image
        elif pushed_at and self._is_old(pushed_at):

            severity = "MEDIUM"
            issue = "Old ECR Image"
            recommendation = (
                "Review and remove this old image if it is no longer required."
            )

        else:

            severity = "LOW"
            issue = "Healthy"
            recommendation = "No action required."

        return Recommendation(
            service="ECR",
            resource_id=image_digest,
            resource_name=repository_name,
            resource_type="Docker Image",
            severity=severity,
            issue=issue,
            recommendation=recommendation,
            estimated_monthly_saving_usd=0,
            region=aws.ecr.meta.region_name,
            status="Available",
        )

    def _is_old(self, pushed_at):

        cutoff = datetime.now(timezone.utc) - timedelta(days=30)

        return pushed_at < cutoff