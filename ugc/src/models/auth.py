from uuid import UUID

from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    id: UUID = Field(..., alias="sub")
