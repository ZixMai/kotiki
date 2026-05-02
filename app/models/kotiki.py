from uuid import UUID

from pydantic import BaseModel


class KotikiItem(BaseModel):
    id: UUID
    name: str


class KotikiList(BaseModel):
    items: list[KotikiItem]


class KotikiCreateUploadResult(BaseModel):
    id: UUID
    name: str
    key: str
