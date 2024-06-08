from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    id: str = Field(..., alias="sub")
