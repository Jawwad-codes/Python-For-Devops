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
    actual_monthly_cost_usd: float


class ScanResult(BaseModel):
    service: str
    actual_cost_usd: float
    findings: list[Recommendation]