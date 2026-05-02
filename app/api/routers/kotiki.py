from io import BytesIO
from os import environ

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_kotiki_service
from app.models.kotiki import KotikiCreateUploadResult, KotikiList
from app.services.kotiki_service import KotikiService

router = APIRouter()


@router.get("/kotiki", response_model=KotikiList, status_code=200)
async def list_kotiki(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: KotikiService = Depends(get_kotiki_service),
):
    items = await service.list_kotiki(limit, offset)
    return {"items": items}


@router.post("/kotiki", response_model=KotikiCreateUploadResult, status_code=201)
async def create_kotik(
    name: str = Form(...),
    token: str = Form(...),
    file: UploadFile = File(...),
    service: KotikiService = Depends(get_kotiki_service),
):
    if token != environ["UPLOAD_TOKEN"]:
        raise HTTPException(status_code=403, detail="Invalid token")
    data = await file.read()
    item = await service.create_kotik_with_upload(name, data, file.content_type)
    return {"id": item["id"], "name": item["name"], "key": item["id"]}


@router.get("/download/{key}", status_code=200)
async def download_file(
    key: str,
    service: KotikiService = Depends(get_kotiki_service),
):
    data, content_type = await service.download_file(key)
    media_type = content_type or "application/octet-stream"
    headers = {"Content-Disposition": f"inline; filename=\"{key}\""}
    return StreamingResponse(BytesIO(data), media_type=media_type, headers=headers)
