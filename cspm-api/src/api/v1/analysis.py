from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import AnalysisCreateReq, AnalysisRes
from src.model.entity import Analysis

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


@router.post("/analysis", response_model=Analysis, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysisReq: AnalysisCreateReq, session: AsyncSession = Depends(get_session)
):
    analysis = Analysis(**analysisReq.model_dump(by_alias=False))
    session.add(analysis)
    await session.commit()
    await session.refresh(analysis)
    return analysis

# {
#     "id": instance["InstanceId"],
#     "state": instance["State"]["Name"],
#     "type": instance["InstanceType"],
#     "instance": instance
# }