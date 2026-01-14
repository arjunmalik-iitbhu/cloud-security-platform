from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import CredentialCreateReq, CredentialRes
from src.model.entity import Credential

router = APIRouter(
    tags=["credentials"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/credentials", response_model=list[CredentialRes])
async def read_credentials(
    offset: int = 0,
    limit: int = 10,
    credential: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Credential)
    if credential:
        query = query.where(col(Credential.name).ilike(f"%{credential}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    credentials = result.all()
    return [CredentialRes(**credential.model_dump()) for credential in credentials]


@router.get("/credential/{credential_id}", response_model=CredentialRes)
async def read_credential(
    credential_id: str, session: AsyncSession = Depends(get_session)
):
    result = await session.exec(
        select(Credential).where(Credential.id == int(credential_id))
    )
    credential = result.first()
    if not credential or not credential.id:
        raise HTTPException(
            status_code=404, detail=f"Credential {credential_id} not found"
        )
    return CredentialRes(**credential.model_dump())


@router.put(
    "/credential/{credential_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_credential(
    credential_id: str, session: AsyncSession = Depends(get_session)
):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post(
    "/credential", response_model=Credential, status_code=status.HTTP_201_CREATED
)
async def create_credential(
    credentialReq: CredentialCreateReq, session: AsyncSession = Depends(get_session)
):
    credential = Credential(**credentialReq.model_dump(by_alias=False))
    session.add(credential)
    await session.commit()
    await session.refresh(credential)
    return credential
