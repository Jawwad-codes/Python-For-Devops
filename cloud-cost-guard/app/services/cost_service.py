from datetime import datetime, timedelta, timezone

from app.aws.clients import aws


class CostService:

    def get_service_cost(self, service_name):

        end_date = datetime.now(timezone.utc).date()

        start_date = end_date - timedelta(days=30)

        response = aws.ce.get_cost_and_usage(
            TimePeriod={
                "Start": start_date.strftime("%Y-%m-%d"),
                "End": end_date.strftime("%Y-%m-%d"),
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [service_name],
                }
            },
        )

        total_cost = 0

        for result in response["ResultsByTime"]:
            amount = result["Total"]["UnblendedCost"]["Amount"]
            total_cost += float(amount)

        return round(total_cost, 2)