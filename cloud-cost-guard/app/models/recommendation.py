from pydantic import BaseModel


class Recommendation(BaseModel):
    service: str
    resource_id: str
    resource_name: str

    resource_type: str

    severity: str

    issue: str

    recommendation: str

    estimated_monthly_saving_usd: float

    region: str

    status: str