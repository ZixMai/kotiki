from fastapi import Depends, Request

from app.repositories.kotiki_repo import KotikiRepository
from app.repositories.s3_repo import S3Repository
from app.services.kotiki_service import KotikiService


def get_s3_session(request: Request):
    return request.app.state.s3_session


def get_s3_settings(request: Request):
    return request.app.state.s3_settings


def get_pg_pool(request: Request):
    return request.app.state.pg_pool


def get_kotiki_repo(pg_pool=Depends(get_pg_pool)):
    return KotikiRepository(pg_pool)


def get_s3_repo(
    s3_session=Depends(get_s3_session),
    s3_settings=Depends(get_s3_settings),
):
    return S3Repository(s3_session, s3_settings)


def get_kotiki_service(
    kotiki_repo=Depends(get_kotiki_repo),
    s3_repo=Depends(get_s3_repo),
):
    return KotikiService(kotiki_repo, s3_repo)
