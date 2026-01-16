from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import AnalysisGetReq, AnalysisRes, ResourceRes
from src.model.entity import Analysis
from sqlalchemy.orm import joinedload

router = APIRouter(
    tags=["analyses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/analyses", response_model=list[AnalysisRes])
async def read_analyses(
    offset: int = 0,
    limit: int = 10,
    analysis: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Analysis)
    if analysis:
        query = query.where(col(Analysis.name).ilike(f"%{analysis}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    analyses = result.all()
    return [AnalysisRes(**analysis.model_dump()) for analysis in analyses]


@router.get("/analysis/{analysis_id}", response_model=AnalysisRes)
async def read_analysis(analysis_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Analysis).where(Analysis.id == int(analysis_id)))
    analysis = result.first()
    if not analysis or not analysis.id:
        raise HTTPException(status_code=404, detail=f"Analysis {analysis_id} not found")
    return AnalysisRes(**analysis.model_dump())


@router.put(
    "/analysis/{analysis_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_analysis(
    analysis_id: str, session: AsyncSession = Depends(get_session)
):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post("/analysis", response_model=AnalysisRes)
async def get_analysis(
    analysisReq: AnalysisGetReq, session: AsyncSession = Depends(get_session)
):
    result = await session.exec(
        select(Analysis)
        .options(
            joinedload(Analysis.resource_id),
        )
        .where(Analysis.credential_id == int(analysisReq.credential_id))
    )
    analyses = result.all()
    if not analyses:
        raise HTTPException(
            status_code=404, detail=f"Analysis of {analysisReq.credential_id} not found"
        )
    resources = [
        ResourceRes(**analysis.resource.model_dump(), **analysis.model_dump())
        for analysis in analyses
    ]
    return AnalysisRes(credential_id=analysisReq.credential_id, resources=resources)
