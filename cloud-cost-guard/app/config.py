from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str = "ap-south-1"
    demo_mode: bool = True


settings = Settings()


INSTANCE_MONTHLY_COST = {
    "t3.micro": 7.50,
    "t3.small": 15.00,
    "t3.medium": 30.00,
    "t3.large": 60.00,
}
