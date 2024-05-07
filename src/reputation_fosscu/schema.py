import uuid
from pydantic import BaseModel, Field


class AirtableResponseSchema(BaseModel):
    name: str = Field(alias="Name")
    discord_username: str = Field(alias="Discord Username")
    xp: float = Field(alias="XP")

    class Config:
        populate_by_name = True
