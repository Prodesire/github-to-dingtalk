from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dingtalk_webhook: str
    dingtalk_secret: str
