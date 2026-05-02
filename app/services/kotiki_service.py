from uuid import uuid4

from app.repositories.kotiki_repo import KotikiRepository
from app.repositories.s3_repo import S3Repository


class KotikiService:
    def __init__(self, kotiki_repo: KotikiRepository, s3_repo: S3Repository):
        self.kotiki_repo = kotiki_repo
        self.s3_repo = s3_repo

    async def list_kotiki(self, limit: int, offset: int):
        return await self.kotiki_repo.list_kotiki(limit, offset)

    async def create_kotik_with_upload(
        self,
        name: str,
        data: bytes,
        content_type: str | None = None,
    ) -> dict:
        kotik_id = str(uuid4())
        await self.s3_repo.upload(kotik_id, data, content_type)
        return await self.kotiki_repo.create_kotik(kotik_id, name)

    async def download_file(self, key: str) -> tuple[bytes, str | None]:
        return await self.s3_repo.download(key)
