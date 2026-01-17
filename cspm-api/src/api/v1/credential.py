from uuid import uuid4
from typing import Optional
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import CredentialCreateReq, CredentialRes
from src.model.entity import Credential, Resource, Cloud, Analysis
from src.utils import fetch_resources
from src.constants import (
    RESOURCE_TYPE_S3,
    RESOURCE_TYPE_EC2,
    AWS_NAME,
    RISK_LOW,
    RISK_HIGH,
    STATUS_RUNNING,
    STATUS_STOPPED,
)

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


async def _get_analyses(
    cloud_name: str,
    credential: Credential,
    resources: list[Resource],
) -> list[Analysis]:
    """
    Updates database with analyses

    Processes resources to find a compliance status based on the following policies:
    1. Policy A (Compute): If an EC2 instance is running AND is public-facing, Mark as "High Risk". Otherwise: "Low Risk".
    2. Policy B (Storage): Mark as "High Risk" if any of the following are true:
        a. Server-Side Encryption is disabled.
        b. The bucket is Publicly Accessible.
        c. Server Access Logging is disabled.
        d. Bucket Versioning is disabled.
    Otherwise: "Low Risk".
    """
    if cloud_name != AWS_NAME:
        return
    analyses = []
    for resource in resources:
        print("resource", resource)
        resource_id = resource["id"]
        resource_type = resource["type"]
        resource_details = json.loads(resource["details"])
        if resource_type == RESOURCE_TYPE_EC2:
            analysis = Analysis(
                credential_id=credential.id,
                resource_id=resource_id,
                current_resource_status=(
                    STATUS_RUNNING
                    if resource_details.get("State", {}).get("Name", "")
                    == STATUS_RUNNING
                    else STATUS_STOPPED
                ),
                current_resource_risk=(
                    RISK_HIGH
                    if resource_details.get("State", {}).get("Name", "") == "running"
                    and resource_details.get("PublicIpAddress", None)
                    else RISK_LOW
                ),
            )
            analyses.append(analysis)
        elif resource_type == RESOURCE_TYPE_S3:
            analysis = Analysis(
                credential_id=credential.id,
                resource_id=resource_id,
                current_resource_status=(
                    STATUS_RUNNING
                    if resource_details.get("BucketRegion", None)
                    and resource_details.get("CreationDate", None)
                    else STATUS_STOPPED
                ),
                current_resource_risk=(
                    RISK_HIGH
                    if not resource_details.get("ServerSideEncryptionConfiguration", {})
                    .get("Rules", [])[0]
                    .get("ApplyServerSideEncryptionByDefault", None)
                    or resource_details.get("PolicyStatus", {}).get("IsPublic", None)
                    or not resource_details.get("LoggingEnabled", {}).get(
                        "TargetBucket", None
                    )
                    or resource_details.get("Versioning", {}).get("Status", None)
                    == "Suspended"
                    else RISK_LOW
                ),
            )
            analyses.append(analysis)
    return analyses


@router.post(
    "/credential", response_model=Credential, status_code=status.HTTP_201_CREATED
)
async def create_credential(
    credentialReq: CredentialCreateReq, session: AsyncSession = Depends(get_session)
):
    cloud_result = await session.exec(
        select(Cloud).where(Cloud.name == credentialReq.cloud_name)
    )
    cloud = cloud_result.first()
    cloud_id = cloud.id
    resources = fetch_resources(
        cloud_id,
        credentialReq.cloud_name,
        {
            "access_key": credentialReq.access_key,
            "secret_access_key": credentialReq.secret_access_key,
            "region": credentialReq.region,
        },
    )
    dumped_resources = []
    for resource in resources:
        session.add(resource)
        await session.commit()
        await session.refresh(resource)
        dumped_resources.append(resource.model_dump())
    await session.refresh(cloud)
    credential = Credential(
        name=str(uuid4()), cloud_id=cloud_id, **credentialReq.model_dump(by_alias=False)
    )
    session.add(credential)
    await session.commit()
    await session.refresh(credential)
    analyses = await _get_analyses(
        credentialReq.cloud_name, credential, dumped_resources
    )
    for analysis in analyses:
        session.add(analysis)
        await session.commit()
    await session.refresh(credential)
    return credential
