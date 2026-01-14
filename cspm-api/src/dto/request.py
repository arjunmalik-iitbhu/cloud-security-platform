from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )

class CredentialCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new credential.
    """

    name: str
    movie_ids: Optional[list[int]] = None


class AnalysisCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new analysis.
    """

    name: str
