from typing import Any

import aioboto3


class S3Repository:
    def __init__(self, session: aioboto3.Session, settings: dict[str, Any]):
        self.session = session
        self.settings = settings

    async def upload(self, key: str, data: bytes, content_type: str | None = None) -> None:
        async with self._client() as s3:
            params = {"Bucket": self.settings["bucket"], "Key": key, "Body": data}
            if content_type:
                params["ContentType"] = content_type
            await s3.put_object(**params)

    async def download(self, key: str) -> tuple[bytes, str | None]:
        async with self._client() as s3:
            response = await s3.get_object(Bucket=self.settings["bucket"], Key=key)
            content_type = response.get("ContentType")
            async with response["Body"] as stream:
                data = await stream.read()
        return data, content_type

    def _client(self):
        return self.session.client(
            "s3",
            endpoint_url=self.settings["endpoint_url"],
            aws_access_key_id=self.settings["aws_access_key_id"],
            aws_secret_access_key=self.settings["aws_secret_access_key"],
            region_name=self.settings["region_name"],
        )
